"""Workplace model (Work experience)."""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Text, ARRAY, JSON, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class Workplace(Base):
    """Candidate work experience."""

    __tablename__ = "workplaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )

    # Company information
    company_name = Column(String(255), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    industry_ids = Column(ARRAY(UUID(as_uuid=True)), default=[])
    company_size = Column(String(50))  # startup, small, medium, large, enterprise

    # Position
    job_title_id = Column(UUID(as_uuid=True), ForeignKey("job_titles.id"))
    position_name = Column(String(255), nullable=False)
    grade = Column(String(20))

    # Period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # NULL = current
    duration_months = Column(Integer)  # Calculated automatically

    # Description
    description = Column(Text)
    achievements = Column(ARRAY(String), default=[])

    # Skills (will be stored in separate table)
    skills = Column(JSON, default=[])  # [{skill_name, category, proficiency}]

    # Standards used
    standards_used = Column(
        JSON, default=[]
    )  # [{standard_id, experience_level}]

    # Project experience
    project_types = Column(
        ARRAY(String), default=[]
    )  # greenfield, legacy, migration, support
    team_size = Column(Integer)
    role = Column(
        String(50)
    )  # individual_contributor, tech_lead, team_lead, manager

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    candidate = relationship("Candidate", back_populates="workplaces")
    job_title = relationship("JobTitle")
    technologies = relationship(
        "WorkplaceTechnology", back_populates="workplace", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Workplace {self.company_name} - {self.position_name}>"


class WorkplaceTechnology(Base):
    """Technologies used in workplace."""

    __tablename__ = "workplace_technologies"

    workplace_id = Column(
        UUID(as_uuid=True), ForeignKey("workplaces.id"), primary_key=True
    )
    technology_id = Column(
        UUID(as_uuid=True), ForeignKey("technologies.id"), primary_key=True
    )
    proficiency = Column(Integer, default=3)  # 1-5
    usage_intensity = Column(
        String(20), default="secondary"
    )  # primary, secondary, occasional

    # Relationships
    workplace = relationship("Workplace", back_populates="technologies")
    technology = relationship("Technology")

    def __repr__(self):
        return f"<WorkplaceTechnology {self.technology_id}>"


# Temporary table for companies (will be expanded later)
class Company(Base):
    """Company model (simplified for MVP)."""

    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    website = Column(String(255))
    size = Column(String(50))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Company {self.name}>"
