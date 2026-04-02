from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# 🔹 Load environment variables
load_dotenv()

# 🔹 Core
from app.core.database import engine, Base
#from app.core.config import get_settings
from app.core.settings import settings

# 🔹 Import all models (IMPORTANT for SQLAlchemy)
from app.models import user, patient, invoice, transaction

# 🔹 Routers
from app.routers import (
    auth,
    patients,
    invoices,
    transactions,
    analytics
)


# ==============================
# 🚀 APP INIT
# ==============================
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# ==============================
# 🌐 CORS CONFIG
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# 🗄️ DATABASE INIT
# ==============================
Base.metadata.create_all(bind=engine)

# ==============================
# 🔌 ROUTERS
# ==============================
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(invoices.router)
app.include_router(transactions.router)
app.include_router(analytics.router)


# ==============================
# ❤️ HEALTH CHECK
# ==============================
@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is running 🚀"
    }