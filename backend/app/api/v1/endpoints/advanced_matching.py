"""Advanced matching and scoring API endpoints."""

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import time

from app.db.database import get_db
from app.models.schemas.advanced_scoring import (
    AdvancedMatchingResult,
    BatchScoringRequest,
    BatchScoringResult,
    SemanticMatchResult,
    CareerAnalysis,
    CulturalFitScore,
    SkillExtraction,
    TextAnalysisResult,
)
from app.models.schemas.scoring import ScoringWeights
from app.services.advanced_scoring_service import AdvancedScoringService
from app.services.text_analysis_service import TextAnalysisService
from app.services.career_analysis_service import CareerAnalysisService
from app.services.candidate_service import CandidateService
from app.services.vacancy_service import VacancyService
from app.db.models.workplace import Workplace

router = APIRouter()


@router.post("/advanced-score", response_model=AdvancedMatchingResult)
def calculate_advanced_score(
    candidate_id: UUID,
    vacancy_id: UUID,
    weights: Optional[ScoringWeights] = None,
    include_ml_features: bool = False,
    db: Session = Depends(get_db),
):
    """
    Calculate advanced matching score with deep analysis.

    Includes:
    - Base scoring (technologies, experience, etc.)
    - Semantic text analysis
    - Career trajectory analysis
    - Cultural fit assessment
    - ML-ready feature extraction
    """
    # Get candidate
    candidate = CandidateService.get(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Get vacancy
    vacancy = VacancyService.get(db, vacancy_id)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )

    # Calculate advanced score
    if weights is None:
        weights = ScoringWeights()

    result = AdvancedScoringService.calculate_advanced_score(
        db=db,
        candidate=candidate,
        vacancy=vacancy,
        weights=weights,
        include_ml_features=include_ml_features,
    )

    return result


@router.post("/batch-score", response_model=BatchScoringResult)
def batch_calculate_scores(
    request: BatchScoringRequest,
    db: Session = Depends(get_db),
):
    """
    Calculate scores for multiple candidates against a single vacancy.

    Useful for:
    - Comparing multiple candidates
    - Bulk candidate evaluation
    - Candidate ranking
    """
    start_time = time.time()

    # Get vacancy
    vacancy = VacancyService.get(db, UUID(request.vacancy_id))
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )

    # Process each candidate
    results = []
    for candidate_id_str in request.candidate_ids:
        try:
            candidate_id = UUID(candidate_id_str)
            candidate = CandidateService.get(db, candidate_id)

            if not candidate:
                continue  # Skip missing candidates

            if request.use_advanced_scoring:
                result = AdvancedScoringService.calculate_advanced_score(
                    db=db,
                    candidate=candidate,
                    vacancy=vacancy,
                    weights=ScoringWeights(),
                    include_ml_features=request.include_ml_features,
                )
                results.append(result)
            else:
                # Use base scoring if advanced not requested
                from app.services.scoring_service import ScoringService
                base_result = ScoringService.calculate_score(db, candidate, vacancy)
                # Would need to wrap this in AdvancedMatchingResult format
                # For now, skip if not using advanced
                continue

        except Exception as e:
            # Log error but continue processing other candidates
            print(f"Error processing candidate {candidate_id_str}: {e}")
            continue

    processing_time = time.time() - start_time

    # Sort results by final score (descending)
    results.sort(key=lambda x: x.final_score, reverse=True)

    return BatchScoringResult(
        vacancy_id=request.vacancy_id,
        results=results,
        processing_time_seconds=round(processing_time, 2),
        total_candidates=len(results),
    )


@router.get("/career-analysis/{candidate_id}", response_model=CareerAnalysis)
def analyze_candidate_career(
    candidate_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Analyze candidate's career trajectory.

    Returns:
    - Career trend (upward, stable, etc.)
    - Role progression
    - Technical growth
    - Red flags and strengths
    - Career stage and potential score
    """
    candidate = CandidateService.get(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Get workplaces
    workplaces = (
        db.query(Workplace)
        .filter(Workplace.candidate_id == candidate_id)
        .all()
    )

    # Analyze career
    analysis = CareerAnalysisService.analyze_career(workplaces, candidate.grade)

    return analysis


@router.post("/text-analysis/extract-skills")
def extract_skills_from_text(
    text: str,
    db: Session = Depends(get_db),
) -> SkillExtraction:
    """
    Extract skills from text using NLP and taxonomy.

    Returns:
    - Technical skills
    - Soft skills
    - Tools and frameworks
    - Methodologies
    """
    extraction = TextAnalysisService.extract_skills(text)

    return SkillExtraction(
        technical_skills=list(extraction.technical_skills),
        soft_skills=list(extraction.soft_skills),
        tools=list(extraction.tools),
        frameworks=list(extraction.frameworks),
        methodologies=list(extraction.methodologies),
    )


@router.post("/text-analysis/similarity")
def calculate_text_similarity(
    text1: str,
    text2: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Calculate semantic similarity between two texts.

    Returns similarity score (0-100).
    """
    similarity = TextAnalysisService.calculate_text_similarity(text1, text2)

    return {
        "similarity_score": similarity,
        "interpretation": (
            "Very similar" if similarity >= 70 else
            "Somewhat similar" if similarity >= 40 else
            "Not very similar"
        ),
    }


@router.get("/matching/recommendations/{vacancy_id}")
def get_matching_recommendations(
    vacancy_id: UUID,
    min_score: float = 60.0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """
    Get recommended candidates for a vacancy.

    Returns candidates sorted by match score, filtered by minimum score.
    """
    # Get vacancy
    vacancy = VacancyService.get(db, vacancy_id)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )

    # Get all candidates (in production, you'd want pagination)
    from app.db.models.candidate import Candidate
    candidates = db.query(Candidate).limit(100).all()

    # Score each candidate
    scored_candidates = []
    for candidate in candidates:
        try:
            result = AdvancedScoringService.calculate_advanced_score(
                db=db,
                candidate=candidate,
                vacancy=vacancy,
                weights=ScoringWeights(),
                include_ml_features=False,
            )

            if result.final_score >= min_score:
                scored_candidates.append({
                    "candidate_id": str(candidate.id),
                    "candidate_name": candidate.full_name,
                    "score": result.final_score,
                    "recommendation": result.recommendation,
                    "match_quality": result.base_score.match_quality,
                    "highlights": result.detailed_strengths[:3],  # Top 3 strengths
                    "concerns": result.detailed_concerns[:3],  # Top 3 concerns
                })
        except Exception as e:
            print(f"Error scoring candidate {candidate.id}: {e}")
            continue

    # Sort by score
    scored_candidates.sort(key=lambda x: x["score"], reverse=True)

    # Limit results
    scored_candidates = scored_candidates[:limit]

    return {
        "vacancy_id": str(vacancy_id),
        "candidates": scored_candidates,
        "total_found": len(scored_candidates),
        "min_score_threshold": min_score,
    }


@router.post("/explain-match")
def explain_match_decision(
    candidate_id: UUID,
    vacancy_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get detailed explanation of match decision.

    Returns comprehensive breakdown of why candidate matches or doesn't match.
    """
    # Get candidate and vacancy
    candidate = CandidateService.get(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    vacancy = VacancyService.get(db, vacancy_id)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )

    # Calculate advanced score
    result = AdvancedScoringService.calculate_advanced_score(
        db=db,
        candidate=candidate,
        vacancy=vacancy,
        weights=ScoringWeights(),
        include_ml_features=False,
    )

    # Build detailed explanation
    return {
        "candidate": {
            "id": str(candidate.id),
            "name": candidate.full_name,
            "grade": candidate.grade,
        },
        "vacancy": {
            "id": str(vacancy.id),
            "position": vacancy.position_name,
            "company": vacancy.company_name,
        },
        "final_score": result.final_score,
        "recommendation": result.recommendation,
        "explanation": result.match_explanation,
        "breakdown": {
            "technical": result.base_score.breakdown.technologies.score,
            "experience": result.base_score.breakdown.experience.score,
            "cultural_fit": result.cultural_fit.overall_fit,
            "semantic_match": result.semantic_match.bio_description_similarity,
            "career_potential": result.career_analysis.potential_score,
        },
        "strengths": result.detailed_strengths,
        "concerns": result.detailed_concerns,
        "career_insights": {
            "stage": result.career_analysis.career_stage,
            "trajectory": result.career_analysis.career_trend.direction,
            "growth_rate": result.career_analysis.career_trend.growth_rate,
            "red_flags": result.career_analysis.red_flags,
        },
        "missing_requirements": result.base_score.missing_critical_requirements,
    }
