import os
import html
import hashlib
import json
import logging
import re
import secrets
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from email.message import EmailMessage
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request as HttpRequest, urlopen

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session, joinedload

load_dotenv()

import ai
import vision
from database import Base, SessionLocal, engine, get_db
from energy import daily_kwh, room_stats, room_status, wasted_hours
from models import Admin, ApprovalRecipient, ApprovalRequest, ApprovalToken, Building, EnergyReading, Equipment, OccupancyApproval, Room
from seed import seed

TARIFF = float(os.getenv("TARIFF_INR_PER_KWH", 8))
CO2_KG_PER_KWH = 0.8
logger = logging.getLogger(__name__)
EMPTY_SECONDS = max(1, int(os.getenv("EMPTY_SECONDS", "20")))
APPROVAL_EXPIRY_MINUTES = max(1, int(os.getenv("APPROVAL_EXPIRY_MINUTES", "30")))
REJECT_COOLDOWN_MINUTES = max(0, int(os.getenv("REJECT_COOLDOWN_MINUTES", "30")))
_empty_since: dict[int, datetime] = {}
_live_people_count: dict[int, int] = {}
_approval_rate: dict[str, list[float]] = defaultdict(list)
_mail_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="ecowatt-mail")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    approval_columns = {column["name"] for column in inspect(engine).get_columns("approval_requests")}
    if "scope" not in approval_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE approval_requests ADD COLUMN scope VARCHAR(20) NOT NULL DEFAULT 'room'"))
    with SessionLocal() as db:
        seed(db)
        legacy_recipients = db.query(ApprovalRecipient).order_by(ApprovalRecipient.id).all()
        for recipient in legacy_recipients:
            address = recipient.email.strip().lower()
            if not db.query(Admin).filter(Admin.email == address).first() and db.query(Admin).count() < 4:
                db.add(Admin(name=address.split("@")[0].replace(".", " ").title(), email=address, active=True))
        db.flush()
        default_admin = os.getenv("MAIL_USER", "").strip().lower()
        if default_admin and not db.query(Admin).filter(Admin.email == default_admin).first() and db.query(Admin).count() < 4:
            db.add(Admin(name=default_admin.split("@")[0].replace(".", " ").title(), email=default_admin, active=True))
        db.commit()
    if not _email_ready():
        logger.warning("SMTP is not configured; approval emails will not be delivered until backend/.env is completed")
    else:
        logger.info("SMTP settings loaded for approval email delivery")
    yield


app = FastAPI(title="EcoWatt 5-Floor Twin API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def campus_payload(db: Session) -> dict:
    buildings = db.query(Building).options(joinedload(Building.rooms).joinedload(Room.equipment)).all()
    b_list = []
    alerts = []
    for b in buildings:
        rooms_out = []
        for r in b.rooms:
            st = room_stats(r)
            status = room_status(st)
            if st["wasted_kwh"] >= 2:
                alerts.append({
                    "building": b.name,
                    "room": r.name,
                    "status": status,
                    "wasted_kwh": st["wasted_kwh"],
                    "message": f"{b.name} - {r.name} wastes {st['wasted_kwh']} kWh/day (Rs {round(st['wasted_kwh'] * TARIFF * 30)}/mo)."
                })
            rooms_out.append({
                "id": r.id,
                "code": r.code,
                "name": r.name,
                "kind": r.kind,
                "x": r.x, "y": r.y, "w": r.w, "h": r.h,
                "occupied_from": r.occupied_from,
                "occupied_to": r.occupied_to,
                "stats": st,
                "status": status,
                "equipment": [
                    {
                        "id": e.id,
                        "name": e.name,
                        "kind": e.kind,
                        "power_kw": e.power_kw,
                        "is_on": e.is_on,
                        "start_hour": e.start_hour,
                        "end_hour": e.end_hour
                    }
                    for e in r.equipment
                ]
            })
        b_list.append({"id": b.id, "floor_level": b.floor_level, "name": b.name, "dept": b.dept, "rooms": rooms_out})
    alerts.sort(key=lambda x: x["wasted_kwh"], reverse=True)
    return {"buildings": b_list, "alerts": alerts}


@app.get("/api/campus")
def get_campus(db: Session = Depends(get_db)):
    return campus_payload(db)


@app.get("/api/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return campus_payload(db)["alerts"]


class ApprovalRecipientsPayload(BaseModel):
    recipients: list[str] = Field(max_length=4)


class OccupancyProposalPayload(BaseModel):
    room_id: int
    room_code: str
    equipment_ids: list[int] = Field(min_length=1, max_length=100)
    equipment_names: list[str] = Field(min_length=1, max_length=100)


class SimulateEmptyPayload(BaseModel):
    room_id: int
    room_code: str
    equipment_ids: list[int] = Field(default_factory=list, max_length=100)
    equipment_names: list[str] = Field(default_factory=list, max_length=100)


class OccupancyResetPayload(BaseModel):
    room_code: str


class ApprovalDecisionPayload(BaseModel):
    token: str
    decision: str


class AdminPayload(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=254)


class AdminActivePayload(BaseModel):
    active: bool


class EquipmentStatePayload(BaseModel):
    room_code: str
    equipment_name: str
    is_on: Optional[bool] = None
    start_hour: Optional[int] = Field(default=None, ge=0, le=23)
    end_hour: Optional[int] = Field(default=None, ge=0, le=24)


def _valid_email(email: str) -> str:
    normalized = email.strip().lower()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", normalized):
        raise HTTPException(status_code=422, detail="Enter a valid email address.")
    return normalized


def _admin_json(admin: Admin) -> dict:
    return {"id": admin.id, "name": admin.name, "email": admin.email, "active": admin.active, "created_at": admin.created_at.isoformat() if admin.created_at else None}


@app.get("/api/admins")
def list_admins(db: Session = Depends(get_db)):
    return [_admin_json(admin) for admin in db.query(Admin).order_by(Admin.id).all()]


@app.post("/api/admins", status_code=201)
def create_admin(req: AdminPayload, db: Session = Depends(get_db)):
    email = _valid_email(req.email)
    if db.query(Admin).count() >= 4:
        raise HTTPException(status_code=409, detail="Maximum 4 admins")
    if db.query(Admin).filter(Admin.email == email).first():
        raise HTTPException(status_code=409, detail="An admin with that email already exists.")
    admin = Admin(name=req.name.strip(), email=email, active=True)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return _admin_json(admin)


@app.delete("/api/admins/{admin_id}")
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.get(Admin, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found.")
    db.delete(admin)
    db.commit()
    return {"deleted": True, "id": admin_id}


@app.patch("/api/admins/{admin_id}")
def set_admin_active(admin_id: int, req: AdminActivePayload, db: Session = Depends(get_db)):
    admin = db.get(Admin, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found.")
    admin.active = req.active
    db.commit()
    db.refresh(admin)
    return _admin_json(admin)


@app.patch("/api/equipment/state")
def update_equipment_state(req: EquipmentStatePayload, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.code == req.room_code).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")
    equipment = db.query(Equipment).filter(Equipment.room_id == room.id, Equipment.name == req.equipment_name).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Fixture not found in that room.")
    changes = req.dict(exclude_unset=True, exclude={"room_code", "equipment_name"})
    for key, value in changes.items():
        setattr(equipment, key, value)
    db.commit()
    return {"room_code": room.code, "equipment_name": equipment.name, "is_on": equipment.is_on}


def _approval_request_json(approval: ApprovalRequest) -> dict:
    fixtures = json.loads(approval.fixtures_json)
    return {
        "id": f"request-{approval.id}", "request_id": approval.id,
        "room_id": approval.twin_room_id, "room_name": approval.room, "scope": approval.scope,
        "floor_level": approval.floor, "equipment_ids": [item["twin_equipment_id"] for item in fixtures],
        "equipment_names": [item["name"] for item in fixtures], "fixtures": fixtures,
        "people_detected": approval.people_detected, "estimated_kw": approval.estimated_kw,
        "estimated_wasted_units": round(approval.estimated_kw, 2),
        "status": approval.status, "created_at": approval.created_at.isoformat(),
        "expires_at": approval.expires_at.isoformat(), "decided_by_email": approval.decided_by_email,
        "decided_at": approval.decided_at.isoformat() if approval.decided_at else None,
    }


def _rate_check(request: Request):
    key = request.client.host if request.client else "unknown"
    now = time.time()
    window = [stamp for stamp in _approval_rate[key] if now - stamp < 60]
    if len(window) >= 30:
        raise HTTPException(status_code=429, detail="Too many approval requests. Try again shortly.")
    window.append(now)
    _approval_rate[key] = window


def _expire_pending(db: Session):
    now = datetime.utcnow()
    db.query(ApprovalRequest).filter(ApprovalRequest.status == "pending", ApprovalRequest.expires_at <= now).update({ApprovalRequest.status: "expired"}, synchronize_session=False)


def _request_link_email(approval_id: int, raw_token: str, admin: Admin, fixtures: list[dict], room: str, floor: int, kw: float):
    base = (os.getenv("PUBLIC_BASE_URL") or os.getenv("APPROVAL_BASE_URL") or "http://localhost:8001").rstrip("/")
    link = f"{base}/api/approvals/{raw_token}"
    safe_room = html.escape(room)
    fixture_rows = "".join(f"<li>{html.escape(item['name'])} (x{item['quantity']}) — {item['power_kw']:.2f} kW</li>" for item in fixtures)
    approve_url = f"{link}?decision=approve"
    reject_url = f"{link}?decision=reject"
    msg = EmailMessage()
    msg["Subject"] = f"Approval needed: {room} has no people but devices are ON"
    msg["From"] = (os.getenv("SMTP_FROM") or os.getenv("MAIL_USER", "")).strip()
    msg["To"] = admin.email
    msg.set_content(f"CCTV detects 0 people while {', '.join(item['name'] for item in fixtures)} are active in {room}. Room fixtures turn off in the 3D twin only after an admin approves.\n\nFloor {floor}; estimated load {kw:.2f} kW; estimated one-hour energy use {kw:.2f} kWh.\nReview: {link}")
    msg.add_alternative(f"""<html><body style='font:16px Arial;color:#172033'><h2>Approval needed: {safe_room}</h2>
<p>Floor {floor} · Time {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} · People detected: 0</p>
<ul>{fixture_rows}</ul><p>Estimated power: <b>{kw:.2f} kW</b><br>Estimated wasted units over one hour: <b>{kw:.2f} kWh</b></p>
<p>CCTV detects 0 people while the listed fixtures are active in {safe_room}. Room fixtures turn off in the 3D twin only after an admin approves.</p>
<p><a href='{html.escape(approve_url, quote=True)}' style='background:#15803d;color:white;padding:14px 24px;text-decoration:none;border-radius:6px'>APPROVE</a>
&nbsp; <a href='{html.escape(reject_url, quote=True)}' style='background:#b91c1c;color:white;padding:14px 24px;text-decoration:none;border-radius:6px'>REJECT</a></p>
<p>Opening either link only shows a confirmation page; a decision is recorded after you confirm it.</p></body></html>""", subtype="html")
    return msg


def _send_request_emails(request_id: int, raw_tokens: dict[int, str]):
    with SessionLocal() as db:
        approval = db.get(ApprovalRequest, request_id)
        if not approval:
            return
        admins = db.query(Admin).filter(Admin.active.is_(True)).order_by(Admin.id).all()
        fixtures = json.loads(approval.fixtures_json)
        futures = []
        for admin in admins:
            raw = raw_tokens.get(admin.id)
            if not raw:
                continue
            message = _request_link_email(request_id, raw, admin, fixtures, approval.room, approval.floor, approval.estimated_kw)
            futures.append(_mail_pool.submit(_deliver_email, message))
    for future in futures:
        sent, error = future.result()
        if not sent:
            logger.error("Occupancy request email delivery failed: %s", error)


def _followup_email(room: str, status: str, decided_by: str):
    with SessionLocal() as db:
        admins = db.query(Admin).filter(Admin.active.is_(True)).all()
        for admin in admins:
            msg = EmailMessage()
            msg["Subject"] = f"Room request {status}: {room}"
            msg["From"] = (os.getenv("SMTP_FROM") or os.getenv("MAIL_USER", "")).strip()
            msg["To"] = admin.email
            msg.set_content(f"Request for {room} was {status} by {decided_by}.")
            _mail_pool.submit(_deliver_email, msg)


def _create_room_request(db: Session, room: Room, twin_room_id: int, force: bool = False, twin_equipment_ids: list[int] | None = None, twin_equipment_names: list[str] | None = None) -> tuple[ApprovalRequest, dict[int, str]] | None:
    now = datetime.utcnow()
    _expire_pending(db)
    existing = db.query(ApprovalRequest).filter(ApprovalRequest.room_id == room.id, ApprovalRequest.status == "pending").first()
    if existing:
        return None
    last_reject = db.query(ApprovalRequest).filter(ApprovalRequest.room_id == room.id, ApprovalRequest.status == "rejected").order_by(ApprovalRequest.decided_at.desc()).first()
    if last_reject and last_reject.decided_at and now - last_reject.decided_at < timedelta(minutes=REJECT_COOLDOWN_MINUTES):
        return None
    building = room.building
    fixtures = db.query(Equipment).filter(Equipment.room_id == room.id, Equipment.is_on.is_(True)).all()
    fixtures = [item for item in fixtures if item.kind not in {"cctv", "electrical"} and "server" not in (item.name or "").lower()]
    if twin_equipment_names is not None:
        requested_names = set(twin_equipment_names)
        fixtures = [item for item in fixtures if item.name in requested_names]
    if not fixtures:
        return None
    twin_by_name = {name: twin_equipment_ids[index] for index, name in enumerate(twin_equipment_names or []) if twin_equipment_ids and index < len(twin_equipment_ids)}
    packed = [{"room_id": room.id, "twin_room_id": twin_room_id, "equipment_id": item.id, "twin_equipment_id": twin_by_name.get(item.name, item.id), "name": item.name, "quantity": item.count or 1, "power_kw": float(item.power_kw or 0)} for item in fixtures]
    approval = ApprovalRequest(room_id=room.id, twin_room_id=twin_room_id, room=room.name, floor=building.floor_level if building else 0,
        fixtures_json=json.dumps(packed), people_detected=0, estimated_kw=sum(item["power_kw"] for item in packed),
        status="pending", created_at=now, expires_at=now + timedelta(minutes=APPROVAL_EXPIRY_MINUTES))
    db.add(approval)
    db.flush()
    raw_tokens = {}
    for admin in db.query(Admin).filter(Admin.active.is_(True)).all():
        raw = secrets.token_urlsafe(32)
        db.add(ApprovalToken(request_id=approval.id, admin_id=admin.id, token_hash=hashlib.sha256(raw.encode()).hexdigest()))
        raw_tokens[admin.id] = raw
    db.commit()
    db.refresh(approval)
    return approval, raw_tokens


def _create_floor_request(db: Session, floor_level: int) -> tuple[ApprovalRequest, dict[int, str]] | None:
    now = datetime.utcnow()
    floor_rooms = db.query(Room).join(Building).filter(Building.floor_level == floor_level).all()
    if not floor_rooms or any(room.id not in _empty_since or now - _empty_since[room.id] < timedelta(seconds=EMPTY_SECONDS) for room in floor_rooms):
        return None
    room_ids = [room.id for room in floor_rooms]
    fixture_rows = db.query(Equipment).filter(Equipment.room_id.in_(room_ids), Equipment.is_on.is_(True)).all()
    fixture_rows = [item for item in fixture_rows if item.kind not in {"cctv", "electrical"} and "server" not in (item.name or "").lower()]
    if not fixture_rows:
        return None
    eligible_rooms = {item.room_id for item in fixture_rows}
    if any(room.id not in eligible_rooms for room in floor_rooms):
        return None
    sentinel = -floor_level - 1
    _expire_pending(db)
    if db.query(ApprovalRequest).filter(ApprovalRequest.room_id == sentinel, ApprovalRequest.status == "pending").first():
        return None
    last_reject = db.query(ApprovalRequest).filter(ApprovalRequest.room_id == sentinel, ApprovalRequest.status == "rejected").order_by(ApprovalRequest.decided_at.desc()).first()
    if last_reject and last_reject.decided_at and now - last_reject.decided_at < timedelta(minutes=REJECT_COOLDOWN_MINUTES):
        return None
    building = floor_rooms[0].building
    packed = [{"room_id": item.room_id, "twin_room_id": item.room_id, "equipment_id": item.id, "twin_equipment_id": item.id, "name": item.name, "quantity": item.count or 1, "power_kw": float(item.power_kw or 0)} for item in fixture_rows]
    approval = ApprovalRequest(room_id=sentinel, twin_room_id=-1, room=f"Floor {floor_level} (all rooms)", scope="floor", floor=floor_level,
        fixtures_json=json.dumps(packed), people_detected=0, estimated_kw=sum(item["power_kw"] for item in packed), status="pending",
        created_at=now, expires_at=now + timedelta(minutes=APPROVAL_EXPIRY_MINUTES))
    db.add(approval)
    db.flush()
    raw_tokens = {}
    for admin in db.query(Admin).filter(Admin.active.is_(True)).all():
        raw = secrets.token_urlsafe(32)
        db.add(ApprovalToken(request_id=approval.id, admin_id=admin.id, token_hash=hashlib.sha256(raw.encode()).hexdigest()))
        raw_tokens[admin.id] = raw
    db.commit()
    db.refresh(approval)
    return approval, raw_tokens


def _email_ready() -> bool:
    username = (os.getenv("SMTP_USERNAME") or os.getenv("MAIL_USER", "")).strip()
    gmail_host = username.lower().endswith("@gmail.com")
    host = (os.getenv("MAIL_HOST") or os.getenv("SMTP_HOST", "")).strip() or ("smtp.gmail.com" if gmail_host else "")
    sender = (os.getenv("SMTP_FROM") or username).strip()
    password = (os.getenv("SMTP_PASSWORD") or os.getenv("MAIL_PASS", "")).strip().strip("\"'").replace(" ", "")
    return bool(host and username and sender and password and os.getenv("MAIL_SERVICE_TOKEN", "").strip())


def _approval_json(approval: OccupancyApproval) -> dict:
    return {
        "id": approval.id,
        "room_id": approval.twin_room_id,
        "room_name": approval.room_name,
        "floor_level": approval.floor_level,
        "equipment_ids": json.loads(approval.twin_equipment_ids),
        "equipment_names": json.loads(approval.equipment_names),
        "status": approval.status,
        "created_at": approval.created_at.isoformat() if approval.created_at else None,
    }


def _email_message_payload(message: EmailMessage) -> dict:
    text_body = ""
    html_body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart() or part.get_content_disposition() == "attachment":
                continue
            content = part.get_content()
            if part.get_content_type() == "text/plain":
                text_body = content
            elif part.get_content_type() == "text/html":
                html_body = content
    else:
        content = message.get_content()
        if message.get_content_subtype() == "html":
            html_body = content
        else:
            text_body = content
    return {
        "from": str(message.get("From", "")),
        "to": str(message.get("To", "")),
        "subject": str(message.get("Subject", "")),
        "text": text_body,
        "html": html_body,
    }


def _deliver_email(message: EmailMessage) -> tuple[bool, str | None]:
    if not _email_ready():
        return False, "Email settings are incomplete. Configure the sender App Password and MAIL_SERVICE_TOKEN in backend/.env."
    service_url = (os.getenv("MAIL_SERVICE_URL") or "http://127.0.0.1:8025").rstrip("/") + "/send"
    token = os.getenv("MAIL_SERVICE_TOKEN", "").strip()
    request = HttpRequest(
        service_url,
        data=json.dumps(_email_message_payload(message)).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=35) as result:
            response = json.loads(result.read().decode("utf-8"))
        if response.get("ok"):
            return True, None
        error = response.get("error") or "Mail service did not return a delivery result."
        logger.error("Mail service delivery failed: %s", error)
        return False, f"Mail service delivery failed: {error}"
    except HTTPError as exc:
        try:
            response = json.loads(exc.read().decode("utf-8"))
        except Exception:
            response = {}
        error = response.get("error") or f"Mail service returned HTTP {exc.code}."
        logger.error("Mail service delivery failed: %s", error)
        return False, f"Mail service delivery failed: {error}"
    except URLError as exc:
        logger.exception("Could not reach the local mail service")
        return False, f"Could not reach mail-service at {service_url}: {exc.reason}. Start it from the mail-service directory with npm start."
    except TimeoutError:
        logger.exception("Mail service request timed out")
        return False, "Mail service timed out while sending the email."
    except Exception as exc:
        logger.exception("Could not send email through Nodemailer")
        return False, f"Nodemailer error ({type(exc).__name__}): {exc or 'delivery failed'}"


def _send_approval_email(recipients: list[str], approval: OccupancyApproval) -> tuple[bool, str | None]:
    public_url = os.getenv("APPROVAL_BASE_URL", "http://localhost:8001").rstrip("/")
    action_url = f"{public_url}/api/approvals/action?token={approval.token}"
    names = ", ".join(json.loads(approval.equipment_names))
    message = EmailMessage()
    message["Subject"] = f"Approval needed: empty room on Floor {approval.floor_level}"
    message["From"] = (os.getenv("SMTP_FROM") or os.getenv("SMTP_USERNAME") or os.getenv("MAIL_USER", "")).strip()
    message["To"] = ", ".join(recipients)
    message.set_content(
        f"The webcam detected no people in {approval.room_name} on Floor {approval.floor_level}, "
        f"while these fixtures are on: {names}.\n\n"
        f"Review and approve or reject the power off request here:\n{action_url}\n\n"
        "Approving turns off the listed room fixtures in the EcoWatt twin."
    )
    return _deliver_email(message)


@app.get("/api/approval-settings")
def get_approval_settings(db: Session = Depends(get_db)):
    recipients = db.query(Admin).filter(Admin.active.is_(True)).order_by(Admin.id).all()
    return {"recipients": [row.email for row in recipients], "email_configured": _email_ready()}


@app.put("/api/approval-settings")
def save_approval_settings(req: ApprovalRecipientsPayload, db: Session = Depends(get_db)):
    recipients = [email.strip().lower() for email in req.recipients if email.strip()]
    if len(recipients) > 4:
        raise HTTPException(status_code=400, detail="You can add up to 4 email addresses.")
    if len(set(recipients)) != len(recipients):
        raise HTTPException(status_code=400, detail="Email addresses must be unique.")
    if any(not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) for email in recipients):
        raise HTTPException(status_code=400, detail="Enter valid email addresses.")
    db.query(Admin).delete()
    db.add_all(Admin(name=email.split("@")[0].replace(".", " ").title(), email=email, active=True) for email in recipients)
    db.commit()
    pending_sent = 0
    pending_errors = []
    return {
        "recipients": recipients,
        "email_configured": _email_ready(),
        "pending_emails_sent": pending_sent,
        "email_error": None,
    }


@app.post("/api/approval-settings/test")
def send_test_email(db: Session = Depends(get_db)):
    recipients = [row.email for row in db.query(Admin).filter(Admin.active.is_(True)).order_by(Admin.id).all()]
    if not recipients:
        raise HTTPException(status_code=400, detail="Add at least one recipient email address first.")
    message = EmailMessage()
    message["Subject"] = "EcoWatt Gmail delivery test"
    message["From"] = (os.getenv("SMTP_FROM") or os.getenv("SMTP_USERNAME") or os.getenv("MAIL_USER", "")).strip()
    message["To"] = ", ".join(recipients)
    message.set_content("This is a test email from EcoWatt Twin. Gmail SMTP is working.")
    sent, error = _deliver_email(message)
    if not sent:
        raise HTTPException(status_code=502, detail=error or "Email delivery failed.")
    return {"sent": True, "recipients": recipients}


@app.post("/api/email/test")
def test_email(request: Request, db: Session = Depends(get_db)):
    _rate_check(request)
    recipients = [row.email for row in db.query(Admin).filter(Admin.active.is_(True)).order_by(Admin.id).all()]
    if not recipients:
        raise HTTPException(status_code=400, detail="Add at least one active admin first.")
    errors = []
    for address in recipients:
        msg = EmailMessage()
        msg["Subject"] = "EcoWatt Twin SMTP delivery test"
        msg["From"] = (os.getenv("SMTP_FROM") or os.getenv("MAIL_USER", "")).strip()
        msg["To"] = address
        msg.set_content("EcoWatt Twin test email. Gmail SMTP delivery is configured.")
        sent, error = _deliver_email(msg)
        if not sent:
            errors.append(f"{address}: {error}")
    if errors:
        raise HTTPException(status_code=502, detail="; ".join(errors))
    return {"sent": True, "recipient_count": len(recipients)}


@app.get("/api/approvals")
def list_approvals(limit: int = 50, db: Session = Depends(get_db)):
    _expire_pending(db)
    db.commit()
    current = db.query(ApprovalRequest).order_by(ApprovalRequest.created_at.desc()).limit(max(1, min(limit, 100))).all()
    approvals = (
        db.query(OccupancyApproval)
        .order_by(OccupancyApproval.created_at.desc())
        .limit(max(1, min(limit, 100)))
        .all()
    )
    legacy_rows = [_approval_json(approval) for approval in approvals]
    return sorted([*[_approval_request_json(item) for item in current], *legacy_rows], key=lambda item: item.get("created_at") or "", reverse=True)[:max(1, min(limit, 100))]


@app.post("/api/simulate-empty")
def simulate_empty(req: SimulateEmptyPayload, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    _rate_check(request)
    room = db.query(Room).options(joinedload(Room.building)).filter(Room.code == req.room_code).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")
    if db.query(ApprovalRequest).filter(ApprovalRequest.room_id == room.id, ApprovalRequest.status == "pending").first():
        raise HTTPException(status_code=409, detail="This room already has a pending approval.")
    _empty_since[room.id] = datetime.utcnow() - timedelta(seconds=EMPTY_SECONDS)
    result = _create_room_request(db, room, req.room_id, force=True, twin_equipment_ids=req.equipment_ids, twin_equipment_names=req.equipment_names)
    if not result:
        raise HTTPException(status_code=409, detail="No active eligible fixtures, or this room is in its rejection cooldown.")
    approval, raw_tokens = result
    background_tasks.add_task(_send_request_emails, approval.id, raw_tokens)
    return _approval_request_json(approval)


@app.get("/api/approvals/{approval_id:int}")
def get_approval(approval_id: int, db: Session = Depends(get_db)):
    approval = db.get(OccupancyApproval, approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found.")
    result = _approval_json(approval)
    result["email_configured"] = _email_ready()
    return result


@app.get("/api/approvals/{token}", response_class=HTMLResponse)
def approval_confirmation(token: str, request: Request, decision: str = "approve", db: Session = Depends(get_db)):
    _rate_check(request)
    if decision not in {"approve", "reject"}:
        decision = "approve"
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    link = db.query(ApprovalToken).filter(ApprovalToken.token_hash == token_hash).first()
    if not link:
        return HTMLResponse("<h1>Request expired or link is invalid.</h1>", status_code=404)
    approval = db.get(ApprovalRequest, link.request_id)
    admin = db.get(Admin, link.admin_id)
    if not approval:
        return HTMLResponse("<h1>Request expired.</h1>", status_code=404)
    if approval.status == "pending" and approval.expires_at <= datetime.utcnow():
        approval.status = "expired"
        db.commit()
    safe_room = html.escape(approval.room)
    if approval.status != "pending":
        message = "Request expired" if approval.status == "expired" else f"Already decided by {html.escape(approval.decided_by_email or 'an admin')} at {html.escape(approval.decided_at.isoformat() if approval.decided_at else 'unknown time')}"
        return HTMLResponse(f"<main><h1>{message}</h1><p>{safe_room}, Floor {approval.floor}</p></main><style>body{{font:16px system-ui;background:#0f172a;color:#e2e8f0;padding:3rem}}main{{max-width:40rem;margin:auto}}</style>")
    button = "Approve power off" if decision == "approve" else "Reject request"
    color = "#15803d" if decision == "approve" else "#b91c1c"
    fixtures = ", ".join(item["name"] for item in json.loads(approval.fixtures_json))
    return HTMLResponse(f"""<!doctype html><html><meta name='viewport' content='width=device-width'><title>EcoWatt approval</title>
<body style='font:16px system-ui;background:#0f172a;color:#e2e8f0;padding:2rem'><main style='max-width:40rem;margin:3rem auto;background:#1e293b;padding:2rem;border-radius:1rem'>
<h1>Confirm {decision}</h1><p>{safe_room}, Floor {approval.floor}</p><p>Fixtures: {html.escape(fixtures)}</p>
<p>This request will be recorded for {html.escape(admin.email if admin else 'this admin')}.</p>
<form method='post' action='/api/approvals/{html.escape(token, quote=True)}'><input type='hidden' name='decision' value='{decision}'/><button style='padding:14px 24px;background:{color};color:white;border:0;border-radius:6px;font-weight:bold'>{button}</button></form>
<p id='result'>This confirmation page does not apply the decision until you press the button.</p></main></body></html>""")


@app.post("/api/approvals/propose")
def propose_occupancy_poweroff(
    req: OccupancyProposalPayload,
    request: Request,
    db: Session = Depends(get_db),
):
    _rate_check(request)
    if len(req.equipment_ids) != len(req.equipment_names) or len(set(req.equipment_ids)) != len(req.equipment_ids):
        raise HTTPException(status_code=400, detail="Equipment details are incomplete or duplicated.")
    room = db.query(Room).options(joinedload(Room.building)).filter(Room.code == req.room_code).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found in the campus database.")

    requested_names = set(req.equipment_names)
    equipment = db.query(Equipment).filter(Equipment.room_id == room.id).all()
    equipment = [item for item in equipment if item.name in requested_names]
    safe_equipment = [
        item for item in equipment
        if item.is_on
        and item.kind not in {"cctv", "electrical"}
        and "server" not in (item.name or "").lower()
    ]
    if not safe_equipment or len(safe_equipment) != len(requested_names):
        raise HTTPException(status_code=400, detail="No eligible active fixtures were found for this room.")

    existing = (
        db.query(OccupancyApproval)
        .filter(OccupancyApproval.room_id == room.id, OccupancyApproval.status == "pending")
        .order_by(OccupancyApproval.created_at.desc())
        .first()
    )
    if existing:
        recipients = [row.email for row in db.query(ApprovalRecipient).order_by(ApprovalRecipient.id).all()]
        email_sent, email_error = (False, "Add at least one recipient email address.")
        if recipients:
            email_sent, email_error = _send_approval_email(recipients, existing)
        return {
            **_approval_json(existing),
            "email_sent": email_sent,
            "email_error": email_error,
            "email_configured": _email_ready(),
            "recipient_count": len(recipients),
        }

    recipients = [row.email for row in db.query(ApprovalRecipient).order_by(ApprovalRecipient.id).all()]
    approval = OccupancyApproval(
        token=secrets.token_urlsafe(32),
        room_id=room.id,
        twin_room_id=req.room_id,
        room_name=room.name,
        floor_level=room.building.floor_level,
        equipment_ids=json.dumps([item.id for item in safe_equipment]),
        twin_equipment_ids=json.dumps(req.equipment_ids),
        equipment_names=json.dumps([item.name for item in safe_equipment]),
        status="pending",
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)

    email_sent, email_error = (False, "Add at least one recipient email address.")
    if recipients:
        email_sent, email_error = _send_approval_email(recipients, approval)
    return {
        **_approval_json(approval),
        "email_sent": email_sent,
        "email_error": email_error,
        "email_configured": _email_ready(),
        "recipient_count": len(recipients),
    }


def _decide_approval(token: str, decision: str, db: Session) -> dict:
    if decision not in {"approve", "reject"}:
        raise HTTPException(status_code=400, detail="Decision must be approve or reject.")
    approval = db.query(OccupancyApproval).filter(OccupancyApproval.token == token).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval link is invalid or expired.")
    if approval.status != "pending":
        return _approval_json(approval)

    if decision == "approve":
        ids = json.loads(approval.equipment_ids)
        db.query(Equipment).filter(
            Equipment.room_id == approval.room_id,
            Equipment.id.in_(ids),
        ).update({Equipment.is_on: False}, synchronize_session=False)
        approval.status = "approved"
    else:
        approval.status = "rejected"
    approval.decided_at = datetime.utcnow()
    db.commit()
    db.refresh(approval)
    return _approval_json(approval)


@app.post("/api/approvals/decision")
def decide_approval(req: ApprovalDecisionPayload, db: Session = Depends(get_db)):
    return _decide_approval(req.token, req.decision, db)


@app.get("/api/approvals/action", response_class=HTMLResponse)
def approval_action_page(token: str, db: Session = Depends(get_db)):
    approval = db.query(OccupancyApproval).filter(OccupancyApproval.token == token).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval link is invalid or expired.")
    room_name = html.escape(approval.room_name)
    equipment = html.escape(", ".join(json.loads(approval.equipment_names)))
    if approval.status != "pending":
        return HTMLResponse(
            f"<main><h1>Request {html.escape(approval.status)}</h1><p>{room_name}, Floor {approval.floor_level}</p></main>"
            "<style>body{font:16px system-ui;background:#0f172a;color:#e2e8f0;padding:4rem}main{max-width:40rem;margin:auto}</style>"
        )
    safe_token = html.escape(token, quote=True)
    return HTMLResponse(f"""<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>EcoWatt occupancy approval</title></head>
<body><main><p>ECOWATT TWIN</p><h1>Room power request</h1><p>No people were detected in <b>{room_name}</b> on Floor {approval.floor_level}.</p>
<p>Approve turning off: {equipment}</p><div><button onclick="decide('approve')">Approve power off</button><button onclick="decide('reject')">Reject</button></div><p id="result" role="status"></p></main>
<style>body{{font:16px system-ui;background:#0f172a;color:#e2e8f0;padding:2rem}}main{{max-width:40rem;margin:4rem auto;background:#1e293b;padding:2rem;border-radius:1rem}}p{{line-height:1.5;color:#cbd5e1}}button{{margin:1rem 1rem 0 0;padding:.8rem 1rem;border:0;border-radius:.5rem;font-weight:700;cursor:pointer}}button:first-child{{background:#22d3ee}}button:last-child{{background:#475569;color:white}}</style>
<script>async function decide(decision){{const result=document.getElementById('result');result.textContent='Saving…';try{{const response=await fetch('/api/approvals/decision',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{token:'{safe_token}',decision}})}});const data=await response.json();if(!response.ok)throw new Error(data.detail||'Could not save decision');result.textContent='Request '+data.status+'. You can close this page.';document.querySelectorAll('button').forEach(button=>button.disabled=true)}}catch(error){{result.textContent=error.message}}}}</script></body></html>""")


@app.post("/api/approvals/{token}", response_class=HTMLResponse)
def decide_request(token: str, request: Request, background_tasks: BackgroundTasks, decision: str = Form(...), db: Session = Depends(get_db)):
    _rate_check(request)
    if decision not in {"approve", "reject"}:
        raise HTTPException(status_code=400, detail="Decision must be approve or reject.")
    link = db.query(ApprovalToken).filter(ApprovalToken.token_hash == hashlib.sha256(token.encode()).hexdigest()).first()
    if not link:
        raise HTTPException(status_code=404, detail="Request expired or link is invalid.")
    approval = db.get(ApprovalRequest, link.request_id)
    admin = db.get(Admin, link.admin_id)
    if not approval or not admin:
        raise HTTPException(status_code=404, detail="Request expired or link is invalid.")
    if approval.status == "pending" and approval.expires_at <= datetime.utcnow():
        approval.status = "expired"
        db.commit()
    if approval.status != "pending" or link.used_at:
        if approval.status == "expired":
            return HTMLResponse("<main><h1>Request expired</h1></main>")
        by = approval.decided_by_email or "an admin"
        when = approval.decided_at.isoformat() if approval.decided_at else "unknown time"
        return HTMLResponse(f"<main><h1>Already decided by {html.escape(by)} at {html.escape(when)}</h1><p>Status: {html.escape(approval.status)}</p></main>")
    decided_at = datetime.utcnow()
    new_status = "approved" if decision == "approve" else "rejected"
    won = db.query(ApprovalRequest).filter(
        ApprovalRequest.id == approval.id,
        ApprovalRequest.status == "pending",
        ApprovalRequest.expires_at > decided_at,
    ).update({
        ApprovalRequest.status: new_status,
        ApprovalRequest.decided_by_email: admin.email,
        ApprovalRequest.decided_at: decided_at,
    }, synchronize_session=False)
    if not won:
        db.refresh(approval)
        if approval.status == "expired":
            return HTMLResponse("<main><h1>Request expired</h1></main>")
        by = approval.decided_by_email or "an admin"
        when = approval.decided_at.isoformat() if approval.decided_at else "unknown time"
        return HTMLResponse(f"<main><h1>Already decided by {html.escape(by)} at {html.escape(when)}</h1><p>Status: {html.escape(approval.status)}</p></main>")
    approval.status = new_status
    approval.decided_by_email = admin.email
    approval.decided_at = decided_at
    link.used_at = decided_at
    if decision == "approve":
        fixtures = json.loads(approval.fixtures_json)
        for room_id in {item["room_id"] for item in fixtures}:
            fixture_ids = [item["equipment_id"] for item in fixtures if item["room_id"] == room_id]
            db.query(Equipment).filter(Equipment.room_id == room_id, Equipment.id.in_(fixture_ids)).update({Equipment.is_on: False}, synchronize_session=False)
    db.commit()
    background_tasks.add_task(_followup_email, approval.room, new_status, admin.email)
    return HTMLResponse(f"<main><h1>Request {approval.status}</h1><p>{html.escape(approval.room)} was decided by {html.escape(admin.email)}. The twin will sync within a few seconds.</p></main>")


@app.post("/api/detect")
async def detect_endpoint(background_tasks: BackgroundTasks, file: UploadFile = File(...), room_id: Optional[int] = Form(None), room_code: Optional[str] = Form(None), equipment_ids: str = Form(""), equipment_names: str = Form(""), db: Session = Depends(get_db)):
    raw = await file.read()
    res = vision.detect(raw)
    needs_verification = res["people"] == 0 and len(res["equipment_visible"]) > 0
    room = None
    if room_code:
        room = db.query(Room).options(joinedload(Room.building)).filter(Room.code == room_code).first()
    elif room_id is not None:
        room = db.query(Room).options(joinedload(Room.building)).filter(Room.id == room_id).first()
    created = None
    if room:
        _live_people_count[room.id] = res["people"]
        if res["people"] > 0:
            _empty_since.pop(room.id, None)
        else:
            started = _empty_since.setdefault(room.id, datetime.utcnow())
            if datetime.utcnow() - started >= timedelta(seconds=EMPTY_SECONDS):
                try:
                    twin_ids = json.loads(equipment_ids) if equipment_ids else []
                    twin_names = json.loads(equipment_names) if equipment_names else None
                except json.JSONDecodeError:
                    raise HTTPException(status_code=400, detail="Fixture information is invalid.")
                result = _create_room_request(db, room, room_id or room.id, twin_equipment_ids=twin_ids, twin_equipment_names=twin_names)
                if result:
                    approval, raw_tokens = result
                    created = _approval_request_json(approval)
                    if raw_tokens:
                        background_tasks.add_task(_send_request_emails, approval.id, raw_tokens)
                floor_result = _create_floor_request(db, room.building.floor_level) if room.building else None
                if floor_result:
                    floor_approval, floor_tokens = floor_result
                    created = _approval_request_json(floor_approval)
                    if floor_tokens:
                        background_tasks.add_task(_send_request_emails, floor_approval.id, floor_tokens)
    return {**res, "room_id": room_id, "needs_verification": needs_verification, "empty_seconds": EMPTY_SECONDS, "approval_request": created}


@app.get("/api/occupancy")
def live_occupancy(db: Session = Depends(get_db)):
    rooms = db.query(Room).options(joinedload(Room.building)).all()
    return [{"room_id": room.id, "room_code": room.code, "room_name": room.name,
        "floor_level": room.building.floor_level if room.building else None,
        "person_count": _live_people_count.get(room.id),
        "empty_since": _empty_since[room.id].isoformat() if room.id in _empty_since else None} for room in rooms]


@app.post("/api/occupancy/reset")
def reset_occupancy(req: OccupancyResetPayload, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.code == req.room_code).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")
    _empty_since.pop(room.id, None)
    _live_people_count.pop(room.id, None)
    return {"reset": True, "room_code": room.code}


class AssistantPayload(BaseModel):
    question: Optional[str] = None
    mode: str = "chat"


@app.post("/api/assistant")
def assistant_endpoint(req: AssistantPayload, db: Session = Depends(get_db)):
    ctx = campus_payload(db)
    return {"reply": ai.ask(ctx, req.question, req.mode)}
