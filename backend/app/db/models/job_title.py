"""Job Title model (Ontology)."""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class JobTitle(Base):
    """
    Hierarchical job title ontology.

    Example:
        developer -> backend -> java
        developer -> frontend -> react
    """

    __tablename__ = "job_titles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("job_titles.id"), nullable=True)
    level = Column(Integer, nullable=False, default=0)  # Depth in hierarchy
    path = Column(
        String(500), nullable=False, index=True
    )  # Materialized path: "developer.backend.java"
    aliases = Column(ARRAY(String), default=[])  # Alternative names
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    parent = relationship("JobTitle", remote_side=[id], backref="children")

    def __repr__(self):
        return f"<JobTitle {self.path}>"
