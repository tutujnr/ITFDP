from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas, auth, database
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import os
import shutil

router = APIRouter()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Auth endpoints
@router.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    created = crud.create_user(db, user)
    return created

@router.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Farmer endpoints
@router.post("/farmers", response_model=schemas.FarmerOut)
def create_farmer(f: schemas.FarmerCreate, db: Session = Depends(database.get_db), current_user=Depends(auth.get_current_user)):
    return crud.create_farmer(db, f)

@router.get("/farmers", response_model=List[schemas.FarmerOut])
def get_farmers(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.list_farmers(db, skip, limit)

# Farms
@router.post("/farms", response_model=schemas.FarmOut)
def create_farm(f: schemas.FarmCreate, db: Session = Depends(database.get_db), current_user=Depends(auth.get_current_user)):
    return crud.create_farm(db, f)

# Harvests
@router.post("/harvests", response_model=schemas.HarvestOut)
def create_harvest(h: schemas.HarvestCreate, db: Session = Depends(database.get_db), current_user=Depends(auth.get_current_user)):
    return crud.create_harvest(db, h)

# Image upload
@router.post("/upload-image")
def upload_image(file: UploadFile = File(...), current_user=Depends(auth.get_current_user)):
    filename = file.filename
    dest_path = os.path.join(UPLOAD_DIR, filename)
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": filename, "path": dest_path}

# Prices
@router.get("/prices", response_model=List[schemas.PriceOut])
def get_prices(limit: int = 50, db: Session = Depends(database.get_db)):
    return crud.latest_prices(db, limit)
