import os
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

load_dotenv()

import ai
import vision
from database import Base, SessionLocal, engine, get_db
from energy import daily_kwh, room_stats, room_status, wasted_hours
from models import Building, EnergyReading, Equipment, Room
from seed import seed

TARIFF = float(os.getenv("TARIFF_INR_PER_KWH", 8))
CO2_KG_PER_KWH = 0.8


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed(db)
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


@app.post("/api/detect")
async def detect_endpoint(file: UploadFile = File(...), room_id: Optional[int] = Form(None)):
    raw = await file.read()
    res = vision.detect(raw)
    needs_verification = res["people"] == 0 and len(res["equipment_visible"]) > 0
    return {**res, "room_id": room_id, "needs_verification": needs_verification}


class AssistantPayload(BaseModel):
    question: Optional[str] = None
    mode: str = "chat"


@app.post("/api/assistant")
def assistant_endpoint(req: AssistantPayload, db: Session = Depends(get_db)):
    ctx = campus_payload(db)
    return {"reply": ai.ask(ctx, req.question, req.mode)}
