from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    floor_level = Column(Integer, default=0)
    dept = Column(String(120))
    rooms = relationship("Room", back_populates="building", cascade="all, delete-orphan")


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    name = Column(String(120), nullable=False)
    kind = Column(String(40))
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)
    w = Column(Integer, default=120)
    h = Column(Integer, default=80)
    occupied_from = Column(Integer, default=9)
    occupied_to = Column(Integer, default=17)
    building = relationship("Building", back_populates="rooms")
    equipment = relationship("Equipment", back_populates="room", cascade="all, delete-orphan")


class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    name = Column(String(100))
    kind = Column(String(40))
    count = Column(Integer, default=1)
    power_kw = Column(Float)
    is_on = Column(Boolean, default=True)
    start_hour = Column(Integer, default=8)
    end_hour = Column(Integer, default=17)
    room = relationship("Room", back_populates="equipment")


class EnergyReading(Base):
    __tablename__ = "energy_readings"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), index=True)
    ts = Column(DateTime, index=True)
    kwh = Column(Float)


class ApprovalRecipient(Base):
    __tablename__ = "approval_recipients"
    id = Column(Integer, primary_key=True)
    email = Column(String(254), nullable=False, unique=True)


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(254), nullable=False, unique=True, index=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class OccupancyApproval(Base):
    __tablename__ = "occupancy_approvals"
    id = Column(Integer, primary_key=True)
    token = Column(String(100), nullable=False, unique=True, index=True)
    room_id = Column(Integer, nullable=False, index=True)
    twin_room_id = Column(Integer, nullable=False)
    room_name = Column(String(120), nullable=False)
    floor_level = Column(Integer, nullable=False)
    equipment_ids = Column(Text, nullable=False)
    twin_equipment_ids = Column(Text, nullable=False)
    equipment_names = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    decided_at = Column(DateTime)


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, nullable=False, index=True)
    twin_room_id = Column(Integer, nullable=False)
    room = Column(String(120), nullable=False)
    scope = Column(String(20), nullable=False, default="room")
    floor = Column(Integer, nullable=False)
    fixtures_json = Column(Text, nullable=False)
    people_detected = Column(Integer, nullable=False, default=0)
    estimated_kw = Column(Float, nullable=False, default=0)
    status = Column(String(20), nullable=False, default="pending", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    decided_by_email = Column(String(254))
    decided_at = Column(DateTime)


class ApprovalToken(Base):
    __tablename__ = "approval_tokens"
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("approval_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    admin_id = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(64), nullable=False, unique=True, index=True)
    used_at = Column(DateTime)
