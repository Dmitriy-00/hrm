"""Pydantic schemas."""

from app.models.schemas.job_title import JobTitleCreate, JobTitleUpdate, JobTitleResponse
from app.models.schemas.technology import TechnologyCreate, TechnologyUpdate, TechnologyResponse
from app.models.schemas.standard import StandardCreate, StandardUpdate, StandardResponse
from app.models.schemas.industry import IndustryCreate, IndustryUpdate, IndustryResponse
from app.models.schemas.candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateListResponse,
    CandidateSearchParams,
)
from app.models.schemas.workplace import (
    WorkplaceCreate,
    WorkplaceUpdate,
    WorkplaceResponse,
    WorkplaceListResponse,
)
from app.models.schemas.vacancy import (
    VacancyCreate,
    VacancyUpdate,
    VacancyResponse,
    VacancyListResponse,
    VacancySearchParams,
    VacancyRequirementsUpdate,
)

__all__ = [
    "JobTitleCreate",
    "JobTitleUpdate",
    "JobTitleResponse",
    "TechnologyCreate",
    "TechnologyUpdate",
    "TechnologyResponse",
    "StandardCreate",
    "StandardUpdate",
    "StandardResponse",
    "IndustryCreate",
    "IndustryUpdate",
    "IndustryResponse",
    "CandidateCreate",
    "CandidateUpdate",
    "CandidateResponse",
    "CandidateListResponse",
    "CandidateSearchParams",
    "WorkplaceCreate",
    "WorkplaceUpdate",
    "WorkplaceResponse",
    "WorkplaceListResponse",
    "VacancyCreate",
    "VacancyUpdate",
    "VacancyResponse",
    "VacancyListResponse",
    "VacancySearchParams",
    "VacancyRequirementsUpdate",
]
