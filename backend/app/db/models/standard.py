"""Standard model (Methodologies, Protocols, Patterns)."""

from sqlalchemy import Column, String, Integer, Text, DateTime, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.db.database import Base


class StandardType(str, enum.Enum):
    """Standard types."""

    METHODOLOGY = "methodology"
    PROTOCOL = "protocol"
    PATTERN = "pattern"
    PRINCIPLE = "principle"
    CERTIFICATION = "certification"


class Standard(Base):
    """
    Standards and methodologies.

    Examples: Agile, Scrum, REST, SOLID, TDD, etc.
    """

    __tablename__ = "standards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    path = Column(String(500), nullable=False)
    description = Column(Text)
    applicable_to = Column(
        ARRAY(UUID(as_uuid=True)), default=[]
    )  # Job title IDs
    related_tools = Column(ARRAY(UUID(as_uuid=True)), default=[])  # Technology IDs
    difficulty = Column(Integer, default=3)  # 1-5
    importance_by_grade = Column(
        JSON, default={}
    )  # {"junior": 50, "middle": 70, "senior": 90}

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Standard {self.name}>"
