"""Candidate schemas."""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, field_validator


class LanguageProficiency(BaseModel):
    """Language proficiency schema."""

    language: str = Field(..., min_length=1, max_length=50)
    proficiency: str = Field(..., pattern="^(A1|A2|B1|B2|C1|C2|native)$")


class SalaryExpectation(BaseModel):
    """Salary expectation schema."""

    min: Optional[int] = Field(None, ge=0)
    max: Optional[int] = Field(None, ge=0)
    currency: str = Field(default="USD", pattern="^(USD|EUR|RUB)$")
    type: str = Field(default="gross", pattern="^(gross|net)$")


class CandidateBase(BaseModel):
    """Base schema for Candidate."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)

    # Professional information
    job_title_id: Optional[UUID] = None
    current_job_title: Optional[str] = Field(None, max_length=255)
    grade: Optional[str] = Field(None, pattern="^(intern|junior|middle|senior|lead|architect)$")

    # Location
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    timezone: Optional[str] = Field(None, max_length=50)
    citizenship: List[str] = Field(default_factory=list)
    relocation: bool = False
    remote_work: bool = True

    # Languages
    languages: List[LanguageProficiency] = Field(default_factory=list)

    # Contacts
    contacts: Dict[str, str] = Field(default_factory=dict)

    # About
    about_me: Optional[str] = None

    # Status
    status: str = Field(default="active", pattern="^(active|passive|not_looking|hired)$")
    available_from: Optional[date] = None


class CandidateCreate(CandidateBase):
    """Schema for creating Candidate."""

    user_id: Optional[UUID] = None


class CandidateUpdate(BaseModel):
    """Schema for updating Candidate."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)

    job_title_id: Optional[UUID] = None
    current_job_title: Optional[str] = Field(None, max_length=255)
    grade: Optional[str] = None

    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    timezone: Optional[str] = Field(None, max_length=50)
    citizenship: Optional[List[str]] = None
    relocation: Optional[bool] = None
    remote_work: Optional[bool] = None

    languages: Optional[List[LanguageProficiency]] = None
    contacts: Optional[Dict[str, str]] = None
    about_me: Optional[str] = None
    status: Optional[str] = None
    available_from: Optional[date] = None


class CandidateSalaryUpdate(BaseModel):
    """Schema for updating candidate salary expectations."""

    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: Optional[str] = Field(None, pattern="^(USD|EUR|RUB)$")
    salary_type: Optional[str] = Field(None, pattern="^(gross|net)$")


class CandidateResponse(CandidateBase):
    """Schema for Candidate response."""

    id: UUID
    user_id: Optional[UUID] = None
    experience_months: int = 0
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    salary_type: str = "gross"
    created_at: datetime
    updated_at: datetime
    last_active: datetime

    class Config:
        from_attributes = True


class CandidateListResponse(BaseModel):
    """Schema for Candidate list response with pagination."""

    items: List[CandidateResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CandidateSearchParams(BaseModel):
    """Schema for candidate search parameters."""

    # Filters
    job_title_ids: Optional[List[UUID]] = None
    technologies: Optional[List[UUID]] = None
    grades: Optional[List[str]] = None
    min_experience_years: Optional[int] = Field(None, ge=0)
    max_experience_years: Optional[int] = Field(None, ge=0)

    # Location
    countries: Optional[List[str]] = None
    cities: Optional[List[str]] = None
    open_to_remote: Optional[bool] = None
    open_to_relocation: Optional[bool] = None

    # Languages
    required_languages: Optional[List[Dict[str, str]]] = None  # [{"language": "English", "min_level": "B2"}]

    # Salary
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None

    # Availability
    availability: Optional[str] = None  # immediate, 2_weeks, 1_month, negotiable
    status: Optional[List[str]] = None  # active, passive

    # Search
    search: Optional[str] = None

    # Pagination
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    # Sorting
    sort_by: str = Field(default="created_at", pattern="^(created_at|experience|last_active|salary_min)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
