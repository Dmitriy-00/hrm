"""Industry model (Ontology)."""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class Industry(Base):
    """
    Industry ontology.

    Example:
        fintech -> blockchain
        healthtech -> telemedicine
    """

    __tablename__ = "industries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("industries.id"), nullable=True)
    description = Column(Text)
    common_tech_stack = Column(
        ARRAY(UUID(as_uuid=True)), default=[]
    )  # Commonly used technologies
    compliance_requirements = Column(ARRAY(String), default=[])  # GDPR, HIPAA, etc.
    typical_challenges = Column(ARRAY(String), default=[])

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    parent = relationship("Industry", remote_side=[id], backref="children")

    def __repr__(self):
        return f"<Industry {self.name}>"
