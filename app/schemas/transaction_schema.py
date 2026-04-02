from pydantic import BaseModel
from datetime import datetime


class TransactionCreate(BaseModel):
    invoice_id: int
    amount: float
    method: str


class TransactionOut(BaseModel):
    id: int
    invoice_id: int
    amount: float
    method: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True