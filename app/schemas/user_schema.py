from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ================= CREATE USER =================
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    contact_number: str = Field(..., min_length=10, max_length=15)
    full_name: Optional[str] = None
    password: str = Field(..., min_length=6)
    confirm_password: str

# ================= LOGIN =================
class UserLogin(BaseModel):
    username: str
    password: str

# ================= RESPONSE =================
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    contact_number: Optional[str]
    full_name: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True


# ================= TOKEN =================
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ================= FORGOT PASSWORD =================
class ForgotPassword(BaseModel):
    email: EmailStr


# ================= RESET PASSWORD =================
class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)