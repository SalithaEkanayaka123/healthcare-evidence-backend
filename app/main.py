from fastapi import FastAPI

# Initialize the FastAPI application for the Healthcare Evidence Backend.
# FastAPI is chosen for this application because:
# - Strict data validation: Pydantic schemas (evidence_schema.py) enforce safe handling of healthcare evidence data
# - Auto-generated API docs: Swagger UI (/docs) for exploring evidence and summary endpoints
# - SQLAlchemy integration: async-friendly design works well with the PostgreSQL database layer (database.py)
# - Structured routing: supports clean separation of evidence routes (evidence_routes.py) and services
# - Evidence summarization: efficient request handling for the summary_service.py workloads
app = FastAPI(
    title="Healthcare Evidence Backend",
    version="1.0.0",
    description="Backend API for healthcare evidence management"
)

# Health check endpoint to verify the service is running
@app.get("/health")
def health_check():
    # Return service status and name
    return{
        "status": "UP",
        "service": "healthcare-evidence-backend"
    }