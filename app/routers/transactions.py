'''



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionCreate, TransactionOut

from app.routers.auth import get_current_user
from app.models.user import User

from app.services.billing_service import apply_payment

router = APIRouter(prefix="/transactions", tags=["transactions"])


# ================= CREATE TRANSACTION =================
@router.post("/", response_model=TransactionOut)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # role check
    if current_user.role not in ["admin", "receptionist"]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to create transactions"
        )

    # apply payment logic (core business logic lives here)
    tx, invoice = apply_payment(
        db=db,
        invoice_id=data.invoice_id,
        amount=data.amount
    )

    return tx


# ================= GET ALL TRANSACTIONS =================
@router.get("/", response_model=List[TransactionOut])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Transaction).all()


# ================= GET SINGLE TRANSACTION =================
@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return tx


# ================= DELETE TRANSACTION =================
@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete transactions"
        )

    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(tx)
    db.commit()

    return {"message": "Transaction deleted successfully"}
'''


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionCreate, TransactionOut

# auth
from app.routers.auth import get_current_user
from app.models.user import User

# service
from app.services.billing_service import apply_payment

router = APIRouter(prefix="/transactions", tags=["transactions"])


# ================= CREATE TRANSACTION =================
@router.post("/", response_model=TransactionOut)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ ROLE CHECK
    if current_user.role not in ["admin", "receptionist"]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to create transactions"
        )

    # ✅ APPLY PAYMENT LOGIC (handles overpayment + status update)
    tx, invoice = apply_payment(
        db=db,
        invoice_id=data.invoice_id,
        amount=data.amount
    )

    return tx


# ================= GET ALL TRANSACTIONS =================
@router.get("/", response_model=List[TransactionOut])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Transaction).order_by(Transaction.created_at.desc()).all()


# ================= FILTER TRANSACTIONS =================
@router.get("/filter", response_model=List[TransactionOut])
def filter_transactions(
    start_date: str = Query(None, description="Format: YYYY-MM-DD"),
    end_date: str = Query(None, description="Format: YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Transaction)

    try:
        if start_date:
            query = query.filter(
                Transaction.created_at >= datetime.fromisoformat(start_date)
            )

        if end_date:
            query = query.filter(
                Transaction.created_at <= datetime.fromisoformat(end_date)
            )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

    return query.order_by(Transaction.created_at.desc()).all()


# ================= GET SINGLE TRANSACTION =================
@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return tx


# ================= DELETE TRANSACTION =================
@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ ONLY ADMIN
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete transactions"
        )

    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(tx)
    db.commit()

    return {"message": "Transaction deleted successfully"}




