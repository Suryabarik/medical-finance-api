from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ================= CREATE =================
class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None

    phone: str = Field(..., min_length=10, max_length=15)
    email: Optional[str] = None

    address: Optional[str] = None
    disease: Optional[str] = None
    blood_group: Optional[str] = None


# ================= UPDATE =================
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    disease: Optional[str] = None
    blood_group: Optional[str] = None


# ================= RESPONSE =================
class PatientOut(BaseModel):
    id: int
    name: str
    age: Optional[int]
    gender: Optional[str]
    phone: str
    email: Optional[str]
    address: Optional[str]
    disease: Optional[str]
    blood_group: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True