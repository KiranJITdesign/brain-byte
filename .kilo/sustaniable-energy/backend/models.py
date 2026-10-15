from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
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
