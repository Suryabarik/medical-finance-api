

'''


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random

from app.core.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice_schema import InvoiceCreate, InvoiceOut

router = APIRouter(prefix="/invoices", tags=["invoices"])

db_dependency = Depends(get_db)


# ================= CREATE INVOICE =================
@router.post("/", response_model=InvoiceOut)
def create_invoice(
    data: InvoiceCreate,
    db: Session = db_dependency
):
    invoice = Invoice(
        patient_id=data.patient_id,
        total_amount=data.total_amount,
        paid_amount=0,
        due_amount=data.total_amount,
        status="pending",
        invoice_number=f"INV-{random.randint(1000, 9999)}"
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


# ================= GET ALL INVOICES =================
@router.get("/", response_model=list[InvoiceOut])
def get_invoices(
    db: Session = db_dependency
):
    return db.query(Invoice).all()


# ================= GET SINGLE INVOICE =================
@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: int,
    db: Session = db_dependency
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice


# ================= DELETE INVOICE =================
@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    db: Session = db_dependency
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice)
    db.commit()

    return {"message": "Invoice deleted successfully"}

'''
'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from typing import List

from app.core.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice_schema import InvoiceCreate, InvoiceOut

# ✅ Auth import
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/invoices", tags=["invoices"])

db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)


# ================= CREATE INVOICE =================
@router.post("/", response_model=InvoiceOut)
def create_invoice(
    data: InvoiceCreate,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    # (optional rule) only admin or analyst can create invoices
    if current_user.role not in ["admin", "analyst"]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to create invoices"
        )

    invoice = Invoice(
        patient_id=data.patient_id,
        total_amount=data.total_amount,
        paid_amount=0,
        due_amount=data.total_amount,
        status="pending",
        invoice_number=f"INV-{random.randint(1000, 9999)}"
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


# ================= GET ALL INVOICES =================
@router.get("/", response_model=List[InvoiceOut])
def get_invoices(
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    return db.query(Invoice).all()


# ================= GET SINGLE INVOICE =================
@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: int,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice


# ================= DELETE INVOICE (ADMIN ONLY) =================
@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    # ✅ ROLE CHECK
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete invoices"
        )

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice)
    db.commit()

    return {"message": "Invoice deleted successfully"}
'''


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from typing import List

from app.core.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice_schema import InvoiceCreate, InvoiceOut

# auth
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/invoices", tags=["invoices"])

db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)


# ================= CREATE INVOICE =================
@router.post("/", response_model=InvoiceOut)
def create_invoice(
    data: InvoiceCreate,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    # role check
    if current_user.role not in ["admin", "analyst"]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to create invoices"
        )

    invoice = Invoice(
        patient_id=data.patient_id,
        total_amount=data.total_amount,
        paid_amount=0,
        due_amount=data.total_amount,
        status="pending",
        invoice_number=f"INV-{random.randint(1000, 9999)}"
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


# ================= GET ALL INVOICES =================
@router.get("/", response_model=List[InvoiceOut])
def get_invoices(
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    return db.query(Invoice).all()


# ================= GET SINGLE INVOICE =================
@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: int,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice


# ================= DELETE INVOICE (ADMIN ONLY) =================
@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    db: Session = db_dependency,
    current_user: User = current_user_dependency
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete invoices"
        )

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice)
    db.commit()

    return {"message": "Invoice deleted successfully"}