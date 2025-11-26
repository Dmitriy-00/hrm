"""Selection (recruitment pipeline) model."""

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.db.database import Base


class SelectionStatus(str, enum.Enum):
    """Selection status."""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class SelectionPriority(str, enum.Enum):
    """Selection priority."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Selection(Base):
    """Recruitment selection process."""

    __tablename__ = "selections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    vacancy_id = Column(UUID(as_uuid=True), ForeignKey("vacancies.id"), nullable=False)
    recruiter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Status
    current_stage = Column(String(50))
    status = Column(String(20), default=SelectionStatus.NEW, index=True)
    priority = Column(String(20), default=SelectionPriority.MEDIUM)

    # Stages: [{stage_id, stage_name, status, scheduled_date, completed_date, feedback}]
    stages = Column(JSON, default=[])

    # History: [{timestamp, action, user_id, details}]
    history = Column(JSON, default=[])

    # Notes: [{author_id, text, created_at}]
    notes = Column(JSON, default=[])

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    candidate = relationship("Candidate")
    vacancy = relationship("Vacancy")
    recruiter = relationship("User")

    def __repr__(self):
        return f"<Selection {self.candidate_id} -> {self.vacancy_id}>"
