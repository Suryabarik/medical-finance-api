from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analytics_service import get_financial_summary

router = APIRouter(prefix="/analytics", tags=["analytics"])

db_dependency = Depends(get_db)


@router.get("/summary")
def summary(db: Session = db_dependency):
    return get_financial_summary(db)