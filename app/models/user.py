'''
from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)

    # Auth
    hashed_password = Column(String(255), nullable=False)

    # Role-based access
    role = Column(String(50), default="viewer")  
    # roles: admin, analyst, viewer

    # Status
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"
'''


from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    # ================= PRIMARY KEY =================
    id = Column(Integer, primary_key=True, index=True)

    # ================= BASIC INFO =================
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    contact_number = Column(String(15), unique=True, nullable=False)
    full_name = Column(String(150), nullable=True)

    # ================= AUTH =================
    hashed_password = Column(String(255), nullable=False)

    # ================= ROLE =================
    role = Column(String(50), default="viewer")  
    # roles: admin, analyst, viewer

    # ================= STATUS =================
    is_active = Column(Boolean, default=True)

    # ================= PASSWORD RESET =================
    reset_token = Column(String(255), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"