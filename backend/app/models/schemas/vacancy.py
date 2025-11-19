"""Vacancy schemas."""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    """Location schema for vacancy."""

    country: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    remote: bool = False
    relocation: bool = False


class LanguageRequirementSchema(BaseModel):
    """Language requirement schema."""

    language: str = Field(..., min_length=1, max_length=50)
    min_level: str = Field(..., pattern="^(A1|A2|B1|B2|C1|C2|native)$")
    required: bool = True


class VacancyRequirementSchema(BaseModel):
    """Technology requirement schema."""

    technology_id: UUID
    importance: str = Field(default="required", pattern="^(required|nice_to_have|plus)$")
    min_experience_years: Optional[int] = Field(None, ge=0)
    proficiency_level: int = Field(default=3, ge=1, le=5)


class VacancyBase(BaseModel):
    """Base schema for Vacancy."""

    # Company
    company_id: UUID
    company_name: str = Field(..., min_length=1, max_length=255)

    # Position
    job_title_id: Optional[UUID] = None
    position_name: str = Field(..., min_length=1, max_length=255)
    grade: Optional[str] = Field(None, pattern="^(junior|middle|senior|lead|architect)$")

    # Experience requirements
    min_experience_years: Optional[int] = Field(None, ge=0)
    max_experience_years: Optional[int] = Field(None, ge=0)

    # Location
    locations: List[LocationSchema] = Field(default_factory=list)
    timezone_requirements: List[str] = Field(default_factory=list)

    # Language requirements
    language_requirements: List[LanguageRequirementSchema] = Field(default_factory=list)

    # Citizenship
    citizenship_allowed: List[str] = Field(default_factory=list)
    citizenship_restricted: List[str] = Field(default_factory=list)

    # Salary
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: str = Field(default="USD", pattern="^(USD|EUR|RUB)$")
    salary_type: str = Field(default="gross", pattern="^(gross|net)$")
    salary_period: str = Field(default="month", pattern="^(month|year)$")
    salary_negotiable: bool = True

    # Status
    status: str = Field(default="active", pattern="^(draft|active|paused|closed|filled)$")
    deadline: Optional[date] = None

    # Description
    description: str = Field(..., min_length=10)
    responsibilities: List[str] = Field(default_factory=list)

    # Interview process
    interview_process: Dict[str, Any] = Field(default_factory=dict)

    # External links
    external_links: List[Dict[str, str]] = Field(default_factory=list)


class VacancyCreate(VacancyBase):
    """Schema for creating Vacancy."""

    created_by: UUID
    requirements: List[VacancyRequirementSchema] = Field(default_factory=list)


class VacancyUpdate(BaseModel):
    """Schema for updating Vacancy."""

    company_id: Optional[UUID] = None
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)

    job_title_id: Optional[UUID] = None
    position_name: Optional[str] = Field(None, min_length=1, max_length=255)
    grade: Optional[str] = None

    min_experience_years: Optional[int] = Field(None, ge=0)
    max_experience_years: Optional[int] = Field(None, ge=0)

    locations: Optional[List[LocationSchema]] = None
    timezone_requirements: Optional[List[str]] = None

    language_requirements: Optional[List[LanguageRequirementSchema]] = None

    citizenship_allowed: Optional[List[str]] = None
    citizenship_restricted: Optional[List[str]] = None

    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: Optional[str] = None
    salary_type: Optional[str] = None
    salary_period: Optional[str] = None
    salary_negotiable: Optional[bool] = None

    status: Optional[str] = None
    deadline: Optional[date] = None

    description: Optional[str] = Field(None, min_length=10)
    responsibilities: Optional[List[str]] = None

    interview_process: Optional[Dict[str, Any]] = None
    external_links: Optional[List[Dict[str, str]]] = None


class VacancyRequirementsUpdate(BaseModel):
    """Schema for updating vacancy requirements."""

    requirements: List[VacancyRequirementSchema]


class VacancyResponse(VacancyBase):
    """Schema for Vacancy response."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    # Include requirements
    requirements: List[VacancyRequirementSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class VacancyListResponse(BaseModel):
    """Schema for Vacancy list response with pagination."""

    items: List[VacancyResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class VacancySearchParams(BaseModel):
    """Schema for vacancy search parameters."""

    # Filters
    job_title_ids: Optional[List[UUID]] = None
    technologies: Optional[List[UUID]] = None
    grades: Optional[List[str]] = None
    min_experience_years: Optional[int] = Field(None, ge=0)
    max_experience_years: Optional[int] = Field(None, ge=0)

    # Location
    countries: Optional[List[str]] = None
    cities: Optional[List[str]] = None
    remote_only: Optional[bool] = None
    relocation_available: Optional[bool] = None

    # Salary
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None

    # Status
    status: Optional[List[str]] = None

    # Company
    company_ids: Optional[List[UUID]] = None

    # Search
    search: Optional[str] = None

    # Pagination
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    # Sorting
    sort_by: str = Field(default="created_at", pattern="^(created_at|salary_min|deadline)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
