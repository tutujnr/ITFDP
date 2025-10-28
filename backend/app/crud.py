from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from typing import List
from sqlalchemy import select, desc

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Auth / Users
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Farmers
def create_farmer(db: Session, f: schemas.FarmerCreate):
    db_f = models.Farmer(name=f.name, phone=f.phone)
    db.add(db_f)
    db.commit()
    db.refresh(db_f)
    return db_f

def list_farmers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Farmer]:
    return db.query(models.Farmer).offset(skip).limit(limit).all()

# Farms
def create_farm(db: Session, data: schemas.FarmCreate):
    db_f = models.Farm(name=data.name, location=data.location, farmer_id=data.farmer_id)
    db.add(db_f)
    db.commit()
    db.refresh(db_f)
    return db_f

# Harvest
def create_harvest(db: Session, data: schemas.HarvestCreate):
    db_h = models.Harvest(farm_id=data.farm_id, weight_kg=data.weight_kg, grade=data.grade, note=data.note)
    db.add(db_h)
    db.commit()
    db.refresh(db_h)
    return db_h

# Prices
def insert_price(db: Session, price_ksh_per_kg: float, source: str = "mombasa_sim", note: str = None):
    p = models.Price(price_ksh_per_kg=price_ksh_per_kg, source=source, note=note)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def latest_prices(db: Session, limit: int = 50):
    return db.query(models.Price).order_by(desc(models.Price.timestamp)).limit(limit).all()
