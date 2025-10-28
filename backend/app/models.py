from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(50), default="farmer")

class Farmer(Base):
    __tablename__ = "farmers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    phone = Column(String(64))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    farms = relationship("Farm", back_populates="farmer")

class Farm(Base):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    location = Column(String(256))
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    farmer = relationship("Farmer", back_populates="farms")
    harvests = relationship("Harvest", back_populates="farm")

class Harvest(Base):
    __tablename__ = "harvests"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    weight_kg = Column(Float)
    grade = Column(String(64))
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    farm = relationship("Farm", back_populates="harvests")

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    price_ksh_per_kg = Column(Float)
    source = Column(String(128))
    note = Column(String(256), nullable=True)
