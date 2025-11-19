"""Advanced scoring schemas with semantic analysis and career trajectory."""

from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.schemas.scoring import CandidateVacancyScore


class SemanticMatchResult(BaseModel):
    """Semantic text matching result."""
    bio_description_similarity: float = Field(..., description="Text similarity 0-100")
    skill_extraction_match: float = Field(..., description="Extracted skill match 0-100")
    keyword_overlap: float = Field(..., description="Keyword overlap percentage 0-100")
    missing_keywords: List[str] = Field(default_factory=list)
    key_phrases_match: List[str] = Field(default_factory=list)


class CareerTrend(BaseModel):
    """Career growth trend."""
    direction: str = Field(..., description="upward, stable, lateral, or downward")
    growth_rate: float = Field(..., description="Growth rate 0-100")
    consistency: float = Field(..., description="Career consistency 0-100")
    specialization_level: float = Field(..., description="Specialization level 0-100")
    leadership_progression: bool
    technical_depth_growth: bool


class RoleProgression(BaseModel):
    """Role progression analysis."""
    role_levels: List[str] = Field(default_factory=list)
    promotions_count: int
    avg_tenure_months: float
    job_hopping_score: float = Field(..., description="Job stability score 0-100")
    role_diversity_score: float = Field(..., description="Role diversity 0-100")


class TechnicalGrowth(BaseModel):
    """Technical skill growth analysis."""
    technologies_learned: int
    tech_stack_modernity: float = Field(..., description="Tech stack modernity 0-100")
    breadth_vs_depth: str = Field(..., description="specialist, generalist, or balanced")
    learning_velocity: float = Field(..., description="Learning speed 0-100")
    tech_leadership: bool


class CareerAnalysis(BaseModel):
    """Comprehensive career analysis."""
    career_trend: CareerTrend
    role_progression: RoleProgression
    technical_growth: TechnicalGrowth
    red_flags: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    career_stage: str = Field(..., description="junior, mid, senior, lead, or executive")
    potential_score: float = Field(..., description="Growth potential 0-100")


class CulturalFitScore(BaseModel):
    """Cultural fit assessment."""
    company_size_fit: float = Field(..., description="Company size fit 0-100")
    work_style_fit: float = Field(..., description="Work style fit 0-100")
    team_environment_fit: float = Field(..., description="Team environment fit 0-100")
    values_alignment: float = Field(..., description="Values alignment 0-100")
    overall_fit: float = Field(..., description="Overall cultural fit 0-100")
    fit_explanation: str


class AdvancedMatchingResult(BaseModel):
    """Comprehensive matching result with advanced analysis."""
    base_score: CandidateVacancyScore
    semantic_match: SemanticMatchResult
    career_analysis: CareerAnalysis
    cultural_fit: CulturalFitScore
    final_score: float = Field(..., description="Final adjusted score 0-100")
    match_explanation: str
    detailed_strengths: List[str] = Field(default_factory=list)
    detailed_concerns: List[str] = Field(default_factory=list)
    recommendation: str = Field(
        ...,
        description="highly_recommend, recommend, consider, or not_recommend"
    )
    ml_features: Dict[str, float] = Field(
        default_factory=dict,
        description="ML-ready features for training"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "final_score": 87.5,
                "match_explanation": "Excellent match with strong technical skills and career trajectory",
                "recommendation": "highly_recommend",
            }
        }


class SkillExtraction(BaseModel):
    """Extracted skills from text."""
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    methodologies: List[str] = Field(default_factory=list)


class TextAnalysisResult(BaseModel):
    """Text analysis result."""
    similarity_score: float = Field(..., description="Similarity 0-100")
    matching_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    sentiment_score: float = Field(..., description="Sentiment 0-100")
    readability_score: float = Field(..., description="Readability 0-100")
    key_phrases: List[str] = Field(default_factory=list)


class BatchScoringRequest(BaseModel):
    """Request for batch scoring multiple candidates."""
    vacancy_id: str
    candidate_ids: List[str] = Field(..., max_length=100)
    use_advanced_scoring: bool = Field(default=True)
    include_ml_features: bool = Field(default=False)


class BatchScoringResult(BaseModel):
    """Result of batch scoring."""
    vacancy_id: str
    results: List[AdvancedMatchingResult]
    processing_time_seconds: float
    total_candidates: int
