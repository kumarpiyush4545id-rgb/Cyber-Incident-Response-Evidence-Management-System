import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.utils.seed_data import seed_sample_data

# Import all models to ensure metadata registration
import app.models

# Import all route modules
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.routes.incidents import router as incidents_router
from app.routes.attack_details import router as attack_router
from app.routes.evidence import router as evidence_router
from app.routes.chain_of_custody import router as coc_router
from app.routes.logs import router as logs_router
from app.routes.threat import router as threat_router
from app.routes.reports import router as reports_router
from app.routes.users import router as users_router
from app.routes.alerts import router as alerts_router

logger = logging.getLogger("cirems.main")
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure directories exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.REPORT_DIR, exist_ok=True)
    os.makedirs(settings.SAMPLE_DATA_DIR, exist_ok=True)
    
    # Initialize database tables
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema synchronized.")

    # Seed initial test & demo data
    logger.info("Checking & seeding enterprise sample dataset...")
    db = SessionLocal()
    try:
        seed_sample_data(db)
        logger.info("Sample dataset ready.")
    except Exception as e:
        logger.error(f"Error seeding sample dataset: {e}")
    finally:
        db.close()

    yield
    # Shutdown
    logger.info("CIREMS Backend shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Centralized Cyber Incident Response & Digital Forensics Evidence Management System. "
        "Provides end-to-end incident tracking, attack vector documentation, cryptographic SHA-256 "
        "evidence integrity verification, append-only chain of custody timelines, Pandas security log analysis, "
        "AI-assisted threat heuristics, and ReportLab forensic PDF report generation."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(incidents_router, prefix=settings.API_V1_STR)
app.include_router(attack_router, prefix=settings.API_V1_STR)
app.include_router(evidence_router, prefix=settings.API_V1_STR)
app.include_router(coc_router, prefix=settings.API_V1_STR)
app.include_router(logs_router, prefix=settings.API_V1_STR)
app.include_router(threat_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(alerts_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OPERATIONAL",
        "documentation": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "timestamp": os.path.exists(settings.UPLOAD_DIR)
    }
