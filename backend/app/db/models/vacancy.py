"""Vacancy model."""

from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.db.database import Base


class VacancyStatus(str, enum.Enum):
    """Vacancy status."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    FILLED = "filled"


class Vacancy(Base):
    """Vacancy model."""

    __tablename__ = "vacancies"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Company
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    company_name = Column(String(255), nullable=False)

    # Position
    job_title_id = Column(UUID(as_uuid=True), ForeignKey("job_titles.id"))
    position_name = Column(String(255), nullable=False)
    grade = Column(String(20), index=True)  # junior, middle, senior, etc.

    # Experience requirements
    min_experience_years = Column(Integer)
    max_experience_years = Column(Integer)

    # Location: [{"country": "Russia", "city": "Moscow", "remote": true}]
    locations = Column(JSON, default=[])
    timezone_requirements = Column(JSON, default=[])

    # Language requirements: [{"language": "English", "min_level": "B2", "required": true}]
    language_requirements = Column(JSON, default=[])

    # Citizenship
    citizenship_allowed = Column(JSON, default=[])
    citizenship_restricted = Column(JSON, default=[])

    # Salary
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(3), default="USD")
    salary_type = Column(String(10), default="gross")  # gross or net
    salary_period = Column(String(10), default="month")  # month or year
    salary_negotiable = Column(Boolean, default=True)

    # Status
    status = Column(String(20), default=VacancyStatus.ACTIVE, index=True)
    deadline = Column(Date)

    # Description
    description = Column(Text, nullable=False)
    responsibilities = Column(JSON, default=[])  # List of responsibilities

    # Interview process
    interview_process = Column(JSON, default={})  # {stages: [...]}

    # External links: [{"source": "hh.ru", "url": "..."}]
    external_links = Column(JSON, default=[])

    # Metadata
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    company = relationship("Company")
    job_title = relationship("JobTitle")
    creator = relationship("User")
    requirements = relationship(
        "VacancyRequirement", back_populates="vacancy", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Vacancy {self.position_name} at {self.company_name}>"
