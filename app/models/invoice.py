from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"))

    invoice_number = Column(String(50), unique=True, index=True)

    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0.0)
    due_amount = Column(Float, default=0.0)

    status = Column(String(50), default="pending")  # paid, partial, pending

    created_at = Column(DateTime, default=datetime.utcnow)