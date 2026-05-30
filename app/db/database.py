from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

DATABASE_URL = settings.database_url

# Create the database engine.
# Engine is responsible for managing the connection between FastAPI and PostgreSQL.
# settings.database_url comes from the .env file.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Create a database session factory.
# autocommit=False means we manually commit transactions using db.commit().
# autoflush=False means SQLAlchemy will not automatically flush changes before every query.
# bind=engine connects this session factory to our PostgreSQL engine.
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    );

# Base class for all SQLAlchemy models.
# Every database model/entity should extend this Base.
Base = declarative_base()

# Dependency function used by FastAPI routes.
# This creates a DB session for each request and closes it after the request is completed.
def get_db():
    db = SessionLocal()

    try:
        # yield gives the database session to the API route/service.
        yield db
    finally:
        # Always close the DB session to avoid connection leaks.
        db.close()

