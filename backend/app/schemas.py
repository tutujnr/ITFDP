from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "farmer"

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class FarmerBase(BaseModel):
    name: str
    phone: Optional[str] = None

class FarmerCreate(FarmerBase):
    pass

class FarmerOut(FarmerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class FarmCreate(BaseModel):
    name: str
    location: Optional[str]
    farmer_id: int

class FarmOut(BaseModel):
    id: int
    name: str
    location: Optional[str]
    farmer_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class HarvestCreate(BaseModel):
    farm_id: int
    weight_kg: float
    grade: Optional[str]
    note: Optional[str]

class HarvestOut(HarvestCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PriceOut(BaseModel):
    id: int
    timestamp: datetime
    price_ksh_per_kg: float
    source: Optional[str]

    class Config:
        orm_mode = True
