# app/services/billing_service.py
'''
from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.models.transaction import Transaction




def apply_payment(db: Session, invoice_id: int, amount: float):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    tx = Transaction(
        invoice_id=invoice_id,
        amount=amount,
        method="cash",
        status="success"
    )

    db.add(tx)

    invoice.paid_amount += amount
    invoice.due_amount = invoice.total_amount - invoice.paid_amount

    # 🔥 IMPORTANT FIX
    if invoice.paid_amount <= 0:
        invoice.status = "pending"
    elif invoice.due_amount == 0:
        invoice.status = "paid"
    else:
        invoice.status = "partial"

    db.commit()
    db.refresh(invoice)

    return tx, invoice
    '''


from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.models.transaction import Transaction


def apply_payment(db: Session, invoice_id: int, amount: float):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # ❌ Prevent overpayment
    if amount > invoice.due_amount:
        raise HTTPException(
            status_code=400,
            detail=f"Payment exceeds due amount. Remaining due: {invoice.due_amount}"
        )

    # ✅ Create transaction
    tx = Transaction(
        invoice_id=invoice_id,
        amount=amount,
        method="cash",
        status="success"
    )

    # ✅ Update invoice
    invoice.paid_amount += amount
    invoice.due_amount -= amount

    # ✅ FIX STATUS LOGIC
    if invoice.due_amount == 0:
        invoice.status = "paid"
    elif invoice.paid_amount > 0:
        invoice.status = "partial"
    else:
        invoice.status = "pending"

    db.add(tx)
    db.commit()
    db.refresh(tx)
    db.refresh(invoice)

    return tx, invoice