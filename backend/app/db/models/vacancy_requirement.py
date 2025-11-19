"""Vacancy requirements model."""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class RequirementImportance(str, enum.Enum):
    """Requirement importance level."""

    REQUIRED = "required"
    NICE_TO_HAVE = "nice_to_have"
    PLUS = "plus"


class VacancyRequirement(Base):
    """Technology requirements for vacancy."""

    __tablename__ = "vacancy_requirements"

    vacancy_id = Column(
        UUID(as_uuid=True), ForeignKey("vacancies.id"), primary_key=True
    )
    technology_id = Column(
        UUID(as_uuid=True), ForeignKey("technologies.id"), primary_key=True
    )

    importance = Column(String(20), default=RequirementImportance.REQUIRED)
    min_experience_years = Column(Integer)
    proficiency_level = Column(Integer, default=3)  # 1-5

    # Relationships
    vacancy = relationship("Vacancy", back_populates="requirements")
    technology = relationship("Technology")

    def __repr__(self):
        return f"<VacancyRequirement {self.vacancy_id} - {self.technology_id}>"
