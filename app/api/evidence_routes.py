from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.evidence_schema import (
    EvidenceCreateRequest,
    EvidenceResponse,
    EvidenceUpdateRequest,
    SummaryResponse
)

from app.services.evidence_service import EvidenceService

# APIRouter instance for all evidence-related endpoints.
# Registered in main.py with a prefix (e.g., /evidence).
router = APIRouter()

# Single shared instance of EvidenceService used across all routes.
service = EvidenceService()

# POST /evidence
# Accepts a validated EvidenceCreateRequest body and creates a new evidence record.
# Returns the created record as EvidenceResponse with HTTP 201 Created.
@router.post("", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
def create_evidence(
    request: EvidenceCreateRequest,
    db: Session = Depends(get_db)  # Injects a database session for this request
):
    return service.create_evidence(db=db, request=request)

# GET /evidence
# Retrieves all evidence records from the database, ordered by most recently created first.
# Returns a list of EvidenceResponse objects.
@router.get("", response_model=list[EvidenceResponse])
def get_all_evidenceRecords(
    db: Session = Depends(get_db)
):
    return service.get_all_evidence(db=db)

# GET /evidence/{evidence_id}
# Retrieves a single evidence record by its ID.
# Returns 404 if no record is found with the given ID.
@router.get("/{evidence_id}", response_model=EvidenceResponse)
def get_evidence_by_id(
    evidence_id: int,
    db: Session = Depends(get_db)
):
    return service.get_evidence_by_id(db=db, evidence_id=evidence_id)

# PUT /evidence/{evidence_id}
# Partially updates an existing evidence record with only the provided fields.
# If content is updated, the stored summary is cleared automatically.
# Returns the updated record as EvidenceResponse.
@router.put("/{evidence_id}", response_model=EvidenceResponse)
def update_evidence(
    evidence_id: int,
    request: EvidenceUpdateRequest,
    db: Session = Depends(get_db)
):
    return service.update_evidence(db, evidence_id, request)

# DELETE /evidence/{evidence_id}
# Deletes an evidence record by its ID.
# Returns HTTP 204 No Content on success; 404 if the record does not exist.
@router.delete("/{evidence_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evidence(
    evidence_id: int,
    db: Session = Depends(get_db)
):
    service.delete_evidence(db, evidence_id)
    return None

# POST /evidence/{evidence_id}/summary
# Triggers summary generation for the specified evidence record via SummaryService.
# Stores the generated summary in the database and returns it as SummaryResponse.
@router.post("/{evidence_id}/summary", response_model=SummaryResponse)
def generate_summary(
    evidence_id: int,
    db: Session = Depends(get_db)
):
    summary = service.generate_summary(db, evidence_id)

    return SummaryResponse(
        evidence_id=evidence_id,
        summary=summary
    )
