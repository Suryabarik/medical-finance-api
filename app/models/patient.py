from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.core.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    # BASIC INFO
    name = Column(String(150), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)

    phone = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(150), nullable=True)

    address = Column(Text, nullable=True)

    # MEDICAL INFO
    disease = Column(String(255), nullable=True)
    blood_group = Column(String(10), nullable=True)

    # RELATION
    created_by = Column(Integer, ForeignKey("users.id"))

    # TIMESTAMP
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Patient(name={self.name}, phone={self.phone})>"