"""Technology model (Ontology)."""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.db.database import Base


class TechnologyCategory(str, enum.Enum):
    """Technology categories."""

    LANGUAGE = "language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    DEVOPS = "devops"
    CLOUD = "cloud"
    TESTING = "testing"
    MOBILE = "mobile"
    DATA = "data"
    ML = "ml"
    GAMEDEV = "gamedev"
    OTHER = "other"


class Technology(Base):
    """
    Technology and tools registry.

    Example:
        Python -> Django -> DRF
        JavaScript -> React -> Next.js
    """

    __tablename__ = "technologies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("technologies.id"), nullable=True)
    path = Column(String(500), nullable=False, index=True)
    tags = Column(ARRAY(String), default=[])
    related_technologies = Column(
        ARRAY(UUID(as_uuid=True)), default=[]
    )  # IDs of related techs
    difficulty_level = Column(Integer, default=3)  # 1-5
    popularity_score = Column(Integer, default=50)  # 0-100
    tech_metadata = Column(JSON, default={})  # official_site, docs, github, version

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    parent = relationship("Technology", remote_side=[id], backref="children")

    def __repr__(self):
        return f"<Technology {self.name}>"
