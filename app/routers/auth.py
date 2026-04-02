'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.security import create_access_token
from passlib.context import CryptContext
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    return {"message": "User created"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username, "role": db_user.role})

    return {"access_token": token}
'''
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr
import secrets

from app.core.database import get_db
from app.models.user import User

# ================= CONFIG =================
router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "CHANGE_THIS_TO_SECURE_KEY"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
RESET_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

db_dependency = Annotated[Session, Depends(get_db)]

# ================= SCHEMAS =================
class SignupSchema(BaseModel):
    username: str
    email: EmailStr
    contact_number: str = Field(..., min_length=10, max_length=15)
    full_name: Optional[str] = None
    password: str = Field(..., min_length=6)
    confirm_password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    contact_number: Optional[str]
    full_name: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

# ================= UTILS =================
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_token(data: dict, expires_delta: timedelta):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user: User):
    return create_token(
        {"sub": user.username, "id": user.id, "role": user.role},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

def create_refresh_token(user: User):
    return create_token(
        {"id": user.id, "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

# ================= CURRENT USER =================
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: db_dependency
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")

        if user_id is None:
            raise HTTPException(401, "Invalid token")

    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(401, "User not found")

    return user

# ================= SIGNUP =================
@router.post("/signup", status_code=201)
async def signup(data: SignupSchema, db: db_dependency):

    if data.password != data.confirm_password:
        raise HTTPException(400, "Passwords do not match")

    existing_user = db.query(User).filter(
        (User.username == data.username) |
        (User.email == data.email) |
        (User.contact_number == data.contact_number)
    ).first()

    if existing_user:
        raise HTTPException(400, "User already exists")

    user_count = db.query(User).count()
    role = "admin" if user_count == 0 else "viewer"

    user = User(
        username=data.username,
        email=data.email,
        contact_number=data.contact_number,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        role=role,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Signup successful", "role": role}

# ================= LOGIN =================
@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
        "token_type": "bearer"
    }

# ================= REFRESH =================
@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: db_dependency):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid refresh token")

    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    user = db.query(User).filter(User.id == payload["id"]).first()

    if not user:
        raise HTTPException(401, "User not found")

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
        "token_type": "bearer"
    }

# ================= ME =================
@router.get("/me", response_model=UserResponse)
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

# ================= FORGOT PASSWORD =================
@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordSchema, db: db_dependency):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(404, "User not found")

    reset_token = secrets.token_urlsafe(32)

    user.reset_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)

    db.commit()

    # 👇 RETURN TOKEN DIRECTLY (FOR TESTING)
    return {
        "message": "Use this token to reset password",
        "reset_token": reset_token
    }

# ================= RESET PASSWORD =================
@router.post("/reset-password")
async def reset_password(data: ResetPasswordSchema, db: db_dependency):

    user = db.query(User).filter(
        User.reset_token == data.token,
        User.reset_token_expiry > datetime.utcnow()
    ).first()

    if not user:
        raise HTTPException(400, "Invalid or expired token")

    user.hashed_password = hash_password(data.new_password)
    user.reset_token = None
    user.reset_token_expiry = None

    db.commit()

    return {"message": "Password reset successful"}

# ================= LOGOUT =================
@router.post("/logout")
async def logout():
    return {"message": "Logout successful"}