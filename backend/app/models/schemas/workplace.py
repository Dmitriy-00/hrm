"""Workplace (work experience) schemas."""

from typing import Optional, List, Dict
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class WorkplaceTechnologySchema(BaseModel):
    """Technology used in workplace."""

    technology_id: UUID
    proficiency: int = Field(default=3, ge=1, le=5)
    usage_intensity: str = Field(default="secondary", pattern="^(primary|secondary|occasional)$")


class WorkplaceSkillSchema(BaseModel):
    """Skill used in workplace."""

    skill_name: str = Field(..., min_length=1, max_length=255)
    skill_category: str = Field(..., min_length=1, max_length=100)
    proficiency: int = Field(default=3, ge=1, le=5)


class StandardUsedSchema(BaseModel):
    """Standard/methodology used in workplace."""

    standard_id: UUID
    experience_level: int = Field(default=3, ge=1, le=5)


class WorkplaceBase(BaseModel):
    """Base schema for Workplace."""

    # Company
    company_name: str = Field(..., min_length=1, max_length=255)
    company_id: Optional[UUID] = None
    industry_ids: List[UUID] = Field(default_factory=list)
    company_size: Optional[str] = Field(None, pattern="^(startup|small|medium|large|enterprise)$")

    # Position
    job_title_id: Optional[UUID] = None
    position_name: str = Field(..., min_length=1, max_length=255)
    grade: Optional[str] = Field(None, pattern="^(intern|junior|middle|senior|lead|architect)$")

    # Period
    start_date: date
    end_date: Optional[date] = None  # None = current

    # Description
    description: Optional[str] = None
    achievements: List[str] = Field(default_factory=list)

    # Skills
    skills: List[WorkplaceSkillSchema] = Field(default_factory=list)

    # Standards
    standards_used: List[StandardUsedSchema] = Field(default_factory=list)

    # Project experience
    project_types: List[str] = Field(default_factory=list)  # greenfield, legacy, migration, support
    team_size: Optional[int] = Field(None, ge=1)
    role: Optional[str] = Field(None, pattern="^(individual_contributor|tech_lead|team_lead|manager)$")

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
        """Validate that end_date is after start_date."""
        if v is not None and 'start_date' in info.data:
            start_date = info.data['start_date']
            if v < start_date:
                raise ValueError('end_date must be after start_date')
        return v


class WorkplaceCreate(WorkplaceBase):
    """Schema for creating Workplace."""

    candidate_id: UUID
    technologies: List[WorkplaceTechnologySchema] = Field(default_factory=list)


class WorkplaceUpdate(BaseModel):
    """Schema for updating Workplace."""

    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    company_id: Optional[UUID] = None
    industry_ids: Optional[List[UUID]] = None
    company_size: Optional[str] = None

    job_title_id: Optional[UUID] = None
    position_name: Optional[str] = Field(None, min_length=1, max_length=255)
    grade: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    description: Optional[str] = None
    achievements: Optional[List[str]] = None

    skills: Optional[List[WorkplaceSkillSchema]] = None
    standards_used: Optional[List[StandardUsedSchema]] = None

    project_types: Optional[List[str]] = None
    team_size: Optional[int] = Field(None, ge=1)
    role: Optional[str] = None

    technologies: Optional[List[WorkplaceTechnologySchema]] = None


class WorkplaceResponse(WorkplaceBase):
    """Schema for Workplace response."""

    id: UUID
    candidate_id: UUID
    duration_months: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    # Technologies (from relationship)
    technologies: List[WorkplaceTechnologySchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class WorkplaceListResponse(BaseModel):
    """Schema for Workplace list response."""

    items: List[WorkplaceResponse]
    total: int
