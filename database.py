import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

logger = logging.getLogger("cirems.database")
logging.basicConfig(level=logging.INFO)

DATABASE_URL = settings.DATABASE_URL

# Attempt connection to Postgres if specified, otherwise fall back to SQLite cleanly
engine = None

def get_engine():
    global engine
    if engine is not None:
        return engine

    # Check if user specified a postgres URL in env
    db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    
    if db_url.startswith("postgresql"):
        try:
            logger.info("Attempting connection to PostgreSQL database...")
            test_engine = create_engine(db_url, pool_pre_ping=True)
            with test_engine.connect() as conn:
                logger.info("Successfully connected to PostgreSQL database.")
            engine = test_engine
            return engine
        except Exception as e:
            if settings.SQLITE_FALLBACK:
                logger.warning(
                    f"Could not connect to PostgreSQL ({e}). "
                    f"Falling back to local SQLite database at ./cirems.db for seamless execution."
                )
                db_url = "sqlite:///./cirems.db"
            else:
                raise e

    # SQLite setup
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {}
    )
    return engine

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
