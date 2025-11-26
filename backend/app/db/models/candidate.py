"""Candidate model."""

from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.db.database import Base


class CandidateGrade(str, enum.Enum):
    """Candidate grade levels."""

    INTERN = "intern"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"
    ARCHITECT = "architect"


class CandidateStatus(str, enum.Enum):
    """Candidate status."""

    ACTIVE = "active"
    PASSIVE = "passive"
    NOT_LOOKING = "not_looking"
    HIRED = "hired"


class Candidate(Base):
    """Candidate profile."""

    __tablename__ = "candidates"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # User reference
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)

    # Basic information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50))

    # Professional information
    job_title_id = Column(UUID(as_uuid=True), ForeignKey("job_titles.id"))
    current_job_title = Column(String(255))
    grade = Column(String(20), index=True)
    experience_months = Column(Integer, default=0)

    # Location
    country = Column(String(100))
    city = Column(String(100))
    timezone = Column(String(50))
    citizenship = Column(JSON, default=[])  # List of countries
    relocation = Column(Boolean, default=False)
    remote_work = Column(Boolean, default=True)

    # Languages: [{"language": "English", "proficiency": "C1"}]
    languages = Column(JSON, default=[])

    # Salary expectations
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(3), default="USD")
    salary_type = Column(String(10), default="gross")  # gross or net

    # Contacts
    contacts = Column(JSON, default={})  # telegram, linkedin, github, etc.

    # About
    about_me = Column(Text)

    # Status
    status = Column(String(20), default=CandidateStatus.ACTIVE, index=True)
    available_from = Column(Date)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_active = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", backref="candidate_profile")
    job_title = relationship("JobTitle")
    workplaces = relationship(
        "Workplace", back_populates="candidate", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Candidate {self.first_name} {self.last_name}>"
