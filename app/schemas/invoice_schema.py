from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InvoiceCreate(BaseModel):
    patient_id: int
    total_amount: float


class InvoiceOut(BaseModel):
    id: int
    patient_id: int
    invoice_number: str
    total_amount: float
    paid_amount: float
    due_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True