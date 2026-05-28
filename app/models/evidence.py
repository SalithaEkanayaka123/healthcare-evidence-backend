from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db.database import Base  # Shared declarative base for all ORM models

# ORM model representing the 'evidence' table in PostgreSQL.
# Each instance of this class corresponds to one row in the table.
class Evidence(Base):
    __tablename__ = "evidence"  # Exact table name created in the database

    # Primary key — auto-incremented unique identifier for each evidence record.
    id = Column(Integer, primary_key=True, index=True)

    # Short title describing the evidence (e.g., study name or article heading).
    title = Column(String(150), nullable=False)

    # Origin of the evidence (e.g., journal name, URL, or institution).
    source = Column(String(100), nullable=False)

    # Full text content of the evidence — stored as unlimited-length text.
    content = Column(Text, nullable=False)

    # Optional AI-generated or manual summary of the evidence content.
    # Populated later by summary_service.py; null until a summary is created.
    summary = Column(Text, nullable=True)

    # Timestamp of when the record was created, automatically set to current UTC time.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
