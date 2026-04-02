'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.patient import Patient
from app.schemas.patient_schema import PatientCreate, PatientOut, PatientUpdate

router = APIRouter(prefix="/patients", tags=["patients"])

db_dependency = Depends(get_db)


# ================= CREATE PATIENT =================
@router.post("/", response_model=PatientOut)
def create_patient(
    data: PatientCreate,
    db: Session = db_dependency
):
    existing = db.query(Patient).filter(Patient.phone == data.phone).first()
    if existing:
        raise HTTPException(400, "Patient already exists")

    patient = Patient(**data.dict(), created_by=1)  # TEMP FIX USER ID

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


# ================= GET ALL PATIENTS =================
@router.get("/", response_model=List[PatientOut])
def get_patients(
    db: Session = db_dependency
):
    return db.query(Patient).all()


# ================= GET SINGLE PATIENT =================
@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(
    patient_id: int,
    db: Session = db_dependency
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(404, "Patient not found")

    return patient


# ================= UPDATE PATIENT =================
@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: int,
    data: PatientUpdate,
    db: Session = db_dependency
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(404, "Patient not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return patient


# ================= DELETE PATIENT =================
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = db_dependency
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(404, "Patient not found")

    db.delete(patient)
    db.commit()

    return {"message": "Patient deleted successfully"}
    '''



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.patient import Patient
from app.schemas.patient_schema import PatientCreate, PatientOut, PatientUpdate

# ✅ Auth import
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/patients", tags=["patients"])

db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)

# ================= CREATE PATIENT =================
@router.post("/", response_model=PatientOut)
def create_patient(
    data: PatientCreate,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    # check duplicate
    existing = db.query(Patient).filter(Patient.phone == data.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient already exists")

    patient = Patient(
        **data.dict(),
        created_by=current_user.id   # ✅ FIXED (no hardcoded user)
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


# ================= GET ALL PATIENTS =================
@router.get("/", response_model=List[PatientOut])
def get_patients(
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    return db.query(Patient).all()


# ================= GET SINGLE PATIENT =================
@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(
    patient_id: int,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


# ================= UPDATE PATIENT =================
@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: int,
    data: PatientUpdate,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return patient


# ================= DELETE PATIENT (ADMIN ONLY) =================
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    # ✅ ROLE CHECK (important for assignment)
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete patients"
        )

    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()

    return {"message": "Patient deleted successfully"}