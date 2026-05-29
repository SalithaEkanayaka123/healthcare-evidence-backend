from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# Used as the request body schema when a client submits a POST request to create a new evidence record.
# Validates and enforces field length constraints before the data reaches the service or database layer.
class EvidenceCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    source: str = Field(..., min_length=2, max_length=100)
    content: str = Field(..., min_length=20)

# Used as the request body schema when a client submits a PATCH/PUT request to update an existing evidence record.
# All fields are optional — only the fields provided by the client will be updated (partial update).
class EvidenceUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    source: Optional[str] = Field(None, min_length=2, max_length=100)
    content: Optional[str] = Field(None, min_length=20)

# Used as the response schema for evidence-related endpoints (e.g., GET, POST, PATCH).
# Defines the exact shape of data returned to the client, including the summary and timestamp.
# from_attributes=True allows Pydantic to read data directly from SQLAlchemy ORM model instances.
class EvidenceResponse(BaseModel):
    id: int
    title: str
    source: str
    content: str
    summary: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True  # Enable parsing from ORM models (e.g., SQLAlchemy)    
    }

# Used as the response schema for the summary generation endpoint.
# Returned after summary_service.py generates or retrieves a summary for a specific evidence record.
class SummaryResponse(BaseModel):
    evidence_id: int
    summary: str