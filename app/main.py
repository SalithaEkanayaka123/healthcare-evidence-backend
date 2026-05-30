from fastapi import FastAPI
from app.core.config import settings
from app.api.evidence_routes import router as evidence_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application for the Healthcare Evidence Backend.
# FastAPI is chosen for this application because:
# - Strict data validation: Pydantic schemas (evidence_schema.py) enforce safe handling of healthcare evidence data
# - Auto-generated API docs: Swagger UI (/docs) for exploring evidence and summary endpoints
# - SQLAlchemy integration: async-friendly design works well with the PostgreSQL database layer (database.py)
# - Structured routing: supports clean separation of evidence routes (evidence_routes.py) and services
# - Evidence summarization: efficient request handling for the summary_service.py workloads
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for healthcare evidence management"
)

app.include_router(
    evidence_router,
    prefix = "/api/evidence",
    tags=["Evidence"]
)

# Health check endpoint to verify the service is running
@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": settings.app_name
    }