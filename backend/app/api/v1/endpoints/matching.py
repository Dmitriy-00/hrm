"""Matching and scoring API endpoints."""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from math import ceil

from app.db.database import get_db
from app.models.schemas.scoring import (
    CandidateVacancyScore,
    MatchingResult,
    MatchingListResponse,
    MatchingParams,
    ScoringWeights,
)
from app.services.scoring_service import ScoringService
from app.services.candidate_service import CandidateService
from app.services.vacancy_service import VacancyService

router = APIRouter()


@router.post("/score", response_model=CandidateVacancyScore)
def calculate_score(
    candidate_id: UUID,
    vacancy_id: UUID,
    weights: Optional[ScoringWeights] = None,
    db: Session = Depends(get_db),
):
    """Calculate matching score between specific candidate and vacancy.

    This endpoint calculates a detailed score breakdown showing how well
    a candidate matches a specific vacancy across multiple dimensions.
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

    # Calculate score
    try:
        if weights is None:
            weights = ScoringWeights()

        score = ScoringService.calculate_score(db, candidate, vacancy, weights)
        return score
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating score: {str(e)}",
        )


@router.get("/candidates/{candidate_id}/vacancies", response_model=MatchingListResponse)
def find_vacancies_for_candidate(
    candidate_id: UUID,
    min_score: float = Query(50.0, ge=0, le=100),
    match_quality: Optional[str] = Query(None, pattern="^(excellent|good|fair|poor)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("score", pattern="^(score|confidence)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    """Find matching vacancies for a candidate.

    Returns a ranked list of vacancies that match the candidate's profile,
    with detailed scoring breakdown and recommendations.
    """
    # Get candidate
    candidate = CandidateService.get(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Get active vacancies
    vacancies = VacancyService.get_active(db, limit=1000)

    # Calculate scores for all vacancies
    results = []
    for vacancy in vacancies:
        try:
            score = ScoringService.calculate_score(db, candidate, vacancy)

            # Apply filters
            if score.total_score < min_score:
                continue

            if match_quality and score.match_quality != match_quality:
                continue

            # Create result
            result = MatchingResult(
                candidate_id=candidate_id,
                vacancy_id=vacancy.id,
                vacancy={
                    "id": str(vacancy.id),
                    "position_name": vacancy.position_name,
                    "company_name": vacancy.company_name,
                    "grade": vacancy.grade,
                    "locations": vacancy.locations,
                    "salary_min": vacancy.salary_min,
                    "salary_max": vacancy.salary_max,
                    "salary_currency": vacancy.salary_currency,
                    "status": vacancy.status,
                },
                score=score,
                highlights=ScoringService.generate_highlights(score),
                concerns=ScoringService.generate_concerns(score),
            )
            results.append(result)
        except Exception as e:
            # Skip vacancies that fail scoring
            continue

    # Sort results
    if sort_by == "confidence":
        results.sort(
            key=lambda x: x.score.confidence_level,
            reverse=(sort_order == "desc")
        )
    else:  # score
        results.sort(
            key=lambda x: x.score.total_score,
            reverse=(sort_order == "desc")
        )

    # Pagination
    total = len(results)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_results = results[start_idx:end_idx]

    return {
        "items": paginated_results,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size) if total > 0 else 0,
    }


@router.get("/vacancies/{vacancy_id}/candidates", response_model=MatchingListResponse)
def find_candidates_for_vacancy(
    vacancy_id: UUID,
    min_score: float = Query(50.0, ge=0, le=100),
    match_quality: Optional[str] = Query(None, pattern="^(excellent|good|fair|poor)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("score", pattern="^(score|confidence)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    """Find matching candidates for a vacancy.

    Returns a ranked list of candidates that match the vacancy requirements,
    with detailed scoring breakdown and recommendations.
    """
    # Get vacancy
    vacancy = VacancyService.get(db, vacancy_id)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )

    # Get active candidates
    candidates, _ = CandidateService.get_all(db, skip=0, limit=10000, status="active")

    # Calculate scores for all candidates
    results = []
    for candidate in candidates:
        try:
            score = ScoringService.calculate_score(db, candidate, vacancy)

            # Apply filters
            if score.total_score < min_score:
                continue

            if match_quality and score.match_quality != match_quality:
                continue

            # Create result
            result = MatchingResult(
                candidate_id=candidate.id,
                vacancy_id=vacancy_id,
                candidate={
                    "id": str(candidate.id),
                    "full_name": candidate.full_name,
                    "grade": candidate.grade,
                    "experience_months": candidate.experience_months,
                    "current_location": candidate.current_location,
                    "salary_min": candidate.salary_min,
                    "salary_max": candidate.salary_max,
                    "status": candidate.status,
                },
                score=score,
                highlights=ScoringService.generate_highlights(score),
                concerns=ScoringService.generate_concerns(score),
            )
            results.append(result)
        except Exception as e:
            # Skip candidates that fail scoring
            continue

    # Sort results
    if sort_by == "confidence":
        results.sort(
            key=lambda x: x.score.confidence_level,
            reverse=(sort_order == "desc")
        )
    else:  # score
        results.sort(
            key=lambda x: x.score.total_score,
            reverse=(sort_order == "desc")
        )

    # Pagination
    total = len(results)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_results = results[start_idx:end_idx]

    return {
        "items": paginated_results,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size) if total > 0 else 0,
    }


@router.post("/batch-score", response_model=MatchingListResponse)
def batch_calculate_scores(
    params: MatchingParams,
    db: Session = Depends(get_db),
):
    """Calculate scores for multiple candidate-vacancy pairs.

    This is a flexible endpoint that can:
    - Find vacancies for a candidate (provide candidate_id)
    - Find candidates for a vacancy (provide vacancy_id)
    - Apply filters and sorting
    """
    if params.candidate_id and params.vacancy_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide either candidate_id OR vacancy_id, not both",
        )

    if not params.candidate_id and not params.vacancy_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either candidate_id or vacancy_id",
        )

    # Route to appropriate endpoint logic
    if params.candidate_id:
        return find_vacancies_for_candidate(
            candidate_id=params.candidate_id,
            min_score=params.min_score,
            match_quality=params.match_quality[0] if params.match_quality else None,
            page=params.page,
            page_size=params.page_size,
            sort_by=params.sort_by,
            sort_order=params.sort_order,
            db=db,
        )
    else:  # vacancy_id
        return find_candidates_for_vacancy(
            vacancy_id=params.vacancy_id,
            min_score=params.min_score,
            match_quality=params.match_quality[0] if params.match_quality else None,
            page=params.page,
            page_size=params.page_size,
            sort_by=params.sort_by,
            sort_order=params.sort_order,
            db=db,
        )
