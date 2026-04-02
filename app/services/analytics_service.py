from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.invoice import Invoice
from app.models.transaction import Transaction


def get_financial_summary(db: Session):

    # total invoices
    total_invoices = db.query(Invoice).count()

    # total revenue (correct)
    total_revenue = db.query(
        func.sum(Transaction.amount)
    ).scalar() or 0

    # ✅ FIX: pending amount should never include negative values
    total_pending = db.query(
        func.sum(
            case(
                (Invoice.due_amount > 0, Invoice.due_amount),
                else_=0
            )
        )
    ).scalar() or 0

    # paid invoices
    total_paid_invoices = db.query(Invoice).filter(
        Invoice.status == "paid"
    ).count()

    # partial invoices
    total_partial_invoices = db.query(Invoice).filter(
        Invoice.status == "partial"
    ).count()

    return {
        "total_invoices": total_invoices,
        "total_revenue": total_revenue,
        "total_pending_amount": total_pending,
        "paid_invoices": total_paid_invoices,
        "partial_invoices": total_partial_invoices
    }