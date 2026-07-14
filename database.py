"""
Database engine + session setup.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

DATABASE_URL = "sqlite:///database/underwriting.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Create all tables if they don't already exist. Call once at app startup."""
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()
