"""Scoring schemas for candidate-vacancy matching."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class TechnologyMatchDetail(BaseModel):
    """Detail of technology match."""

    technology_id: UUID
    technology_name: str
    candidate_proficiency: int
    required_proficiency: int
    candidate_experience_months: int
    required_experience_months: int
    importance: str  # required, nice_to_have, plus
    match_score: float  # 0-100


class TechnologiesBreakdown(BaseModel):
    """Technologies matching breakdown."""

    score: float  # 0-100
    matched: int  # Number of matched technologies
    required: int  # Number of required technologies
    details: List[TechnologyMatchDetail] = Field(default_factory=list)


class ExperienceBreakdown(BaseModel):
    """Experience matching breakdown."""

    score: float  # 0-100
    candidate_months: int
    candidate_years: float
    required_min_months: int
    required_max_months: Optional[int]
    required_min_years: float
    required_max_years: Optional[float]


class SkillsBreakdown(BaseModel):
    """Skills matching breakdown."""

    score: float  # 0-100
    matched: int
    required: int
    missing: List[str] = Field(default_factory=list)


class StandardsBreakdown(BaseModel):
    """Standards matching breakdown."""

    score: float  # 0-100
    matched: int
    required: int


class IndustryBreakdown(BaseModel):
    """Industry matching breakdown."""

    score: float  # 0-100
    has_experience: bool
    experience_months: int


class LanguageMatch(BaseModel):
    """Language match detail."""

    language: str
    candidate_level: str
    required_level: str
    meets_requirement: bool


class LanguagesBreakdown(BaseModel):
    """Languages matching breakdown."""

    score: float  # 0-100
    matched: List[LanguageMatch] = Field(default_factory=list)
    missing: List[str] = Field(default_factory=list)


class LocationBreakdown(BaseModel):
    """Location compatibility breakdown."""

    score: float  # 0-100
    compatible: bool
    details: str


class SalaryBreakdown(BaseModel):
    """Salary compatibility breakdown."""

    score: float  # 0-100
    candidate_min: Optional[int]
    candidate_max: Optional[int]
    vacancy_min: Optional[int]
    vacancy_max: Optional[int]
    overlap: bool
    details: str


class BonusPoint(BaseModel):
    """Bonus point detail."""

    reason: str
    points: float


class ScoreBreakdown(BaseModel):
    """Complete score breakdown."""

    technologies: TechnologiesBreakdown
    experience: ExperienceBreakdown
    skills: SkillsBreakdown
    standards: StandardsBreakdown
    industry: IndustryBreakdown
    languages: LanguagesBreakdown
    location: LocationBreakdown
    salary: SalaryBreakdown


class CandidateVacancyScore(BaseModel):
    """Candidate-vacancy matching score."""

    candidate_id: UUID
    vacancy_id: UUID
    total_score: float = Field(..., ge=0, le=100)  # 0-100

    breakdown: ScoreBreakdown

    # Additional metrics
    confidence_level: float = Field(..., ge=0, le=100)  # Confidence in the score
    missing_critical_requirements: List[str] = Field(default_factory=list)
    bonus_points: List[BonusPoint] = Field(default_factory=list)

    # Match quality
    match_quality: str = Field(..., pattern="^(excellent|good|fair|poor)$")

    # Timestamps
    calculated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class ScoringWeights(BaseModel):
    """Configurable scoring weights."""

    technologies: int = Field(default=40, ge=0, le=100)
    experience: int = Field(default=20, ge=0, le=100)
    skills: int = Field(default=15, ge=0, le=100)
    standards: int = Field(default=10, ge=0, le=100)
    industry: int = Field(default=5, ge=0, le=100)
    languages: int = Field(default=5, ge=0, le=100)
    location: int = Field(default=3, ge=0, le=100)
    salary: int = Field(default=2, ge=0, le=100)


class MatchingResult(BaseModel):
    """Result of matching with score."""

    candidate_id: Optional[UUID] = None
    vacancy_id: Optional[UUID] = None
    candidate: Optional[Dict[str, Any]] = None  # Candidate data
    vacancy: Optional[Dict[str, Any]] = None  # Vacancy data
    score: CandidateVacancyScore
    highlights: List[str] = Field(default_factory=list)  # What matched well
    concerns: List[str] = Field(default_factory=list)  # What's missing
    recommendation: Optional[str] = None  # AI-generated recommendation


class MatchingListResponse(BaseModel):
    """List of matching results with pagination."""

    items: List[MatchingResult]
    total: int
    page: int
    page_size: int
    total_pages: int


class MatchingParams(BaseModel):
    """Parameters for matching."""

    # For finding vacancies for candidate
    candidate_id: Optional[UUID] = None

    # For finding candidates for vacancy
    vacancy_id: Optional[UUID] = None

    # Filters
    min_score: float = Field(default=50.0, ge=0, le=100)
    match_quality: Optional[List[str]] = None  # excellent, good, fair, poor

    # Pagination
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    # Sorting
    sort_by: str = Field(default="score", pattern="^(score|confidence)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
