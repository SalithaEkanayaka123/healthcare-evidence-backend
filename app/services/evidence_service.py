import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.evidence import Evidence
from app.schemas.evidence_schema import EvidenceCreateRequest, EvidenceUpdateRequest
from app.services.summary_service import SummaryService

logger = logging.getLogger(__name__)

# Service class that handles all business logic for healthcare evidence records.
# Called by evidence_routes.py and interacts with the database via SQLAlchemy sessions.
class EvidenceService:

    def __init__(self):
        # Instantiate SummaryService to delegate summary generation logic.
        self.summary_service = SummaryService()
    
    # Creates a new evidence record in the database from the validated request data.
    # Commits the record and refreshes it to include DB-generated fields (e.g., id, created_at).
    def create_evidence(self, db: Session, request: EvidenceCreateRequest) -> Evidence:

        logger.info("Creating evidence record with title=%s", request.title)
        evidence = Evidence(
            title=request.title,
            source=request.source,
            content=request.content
        )

        db.add(evidence)       # Stage the new record for insertion
        db.commit()            # Persist the record to the database
        db.refresh(evidence)   # Reload the record to get DB-generated values

        logger.info("Evidence record created successfully with id=%s", evidence.id)

        return evidence
    
    # Retrieves all evidence records from the database, ordered by most recently created first.
    def get_all_evidence(self, db: Session) -> list[Evidence]:
        logger.info("Fetching all evidence records")

        evidence_records = db.query(Evidence).order_by(Evidence.created_at.desc()).all()

        logger.info("Fetched %s evidence records", len(evidence_records))

        return evidence_records
    
    # Retrieves a single evidence record by its ID.
    # Raises a 404 HTTPException if no record is found with the given ID.
    def get_evidence_by_id(self, db: Session, evidence_id: int) -> Evidence:
        logger.info("Fetching evidence record with id=%s", evidence_id)

        evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()

        if evidence is None:
            logger.warning("Evidence record not found with id=%s", evidence_id)
            raise HTTPException(
                status_code=404,
                detail="Evidence record not found"
            )

        return evidence
    
    # Partially updates an existing evidence record with only the fields provided in the request.
    # If content is updated, the existing summary is cleared since it is no longer valid.
    def update_evidence(self, db: Session, evidence_id: int, request: EvidenceUpdateRequest) -> Evidence:
        evidence = self.get_evidence_by_id(db, evidence_id=evidence_id)

        if request.title is not None:
            evidence.title = request.title
        
        if request.source is not None:
            evidence.source = request.source
        
        if request.content is not None:
            evidence.content = request.content
            evidence.summary = None  # Invalidate the existing summary when content changes
        
        db.commit()
        db.refresh(evidence)

        return evidence
    
    # Deletes an evidence record from the database by its ID.
    # Raises a 404 HTTPException via get_evidence_by_id if the record does not exist.
    def delete_evidence(self, db: Session, evidence_id: int) -> None:
        evidence = self.get_evidence_by_id(db, evidence_id)

        db.delete(evidence)
        db.commit()

    # Generates and stores a summary for an evidence record using SummaryService.
    # Updates the summary field in the database and returns the generated summary string.
    def generate_summary(self, db: Session, evidence_id: int) -> str:
        logger.info("Generating summary for evidence id=%s", evidence_id)

        evidence = self.get_evidence_by_id(db, evidence_id)

        # Delegate summary generation to SummaryService and store the result
        evidence.summary = self.summary_service.generate_summary(
            title=evidence.title,
            content=evidence.content
        )

        db.commit()
        db.refresh(evidence)

        logger.info("Summary generated successfully for evidence id=%s", evidence_id)

        return evidence.summary