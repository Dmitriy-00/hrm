"""Candidates API endpoints."""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from math import ceil

from app.db.database import get_db
from app.models.schemas.candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateListResponse,
    CandidateSearchParams,
    CandidateSalaryUpdate,
)
from app.services.candidate_service import CandidateService

router = APIRouter()


@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
def create_candidate(
    schema: CandidateCreate,
    db: Session = Depends(get_db),
):
    """Create new candidate."""
    try:
        candidate = CandidateService.create(db, schema)
        return candidate
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=CandidateListResponse)
def get_candidates(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all candidates with optional search."""
    candidates, total = CandidateService.get_all(db, skip=skip, limit=limit, search=search)

    return {
        "items": candidates,
        "total": total,
        "page": (skip // limit) + 1,
        "page_size": limit,
        "total_pages": ceil(total / limit) if total > 0 else 0,
    }


@router.post("/search", response_model=CandidateListResponse)
def search_candidates(
    params: CandidateSearchParams,
    db: Session = Depends(get_db),
):
    """Advanced search for candidates."""
    candidates, total = CandidateService.search(db, params)

    return {
        "items": candidates,
        "total": total,
        "page": params.page,
        "page_size": params.page_size,
        "total_pages": ceil(total / params.page_size) if total > 0 else 0,
    }


@router.get("/statistics")
def get_candidate_statistics(db: Session = Depends(get_db)):
    """Get candidate statistics."""
    stats = CandidateService.get_statistics(db)
    return stats


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(
    candidate_id: UUID,
    db: Session = Depends(get_db),
):
    """Get candidate by ID."""
    candidate = CandidateService.get(db, candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Update last active timestamp
    CandidateService.update_last_active(db, candidate_id)

    return candidate


@router.get("/email/{email}", response_model=CandidateResponse)
def get_candidate_by_email(
    email: str,
    db: Session = Depends(get_db),
):
    """Get candidate by email."""
    candidate = CandidateService.get_by_email(db, email)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(
    candidate_id: UUID,
    schema: CandidateUpdate,
    db: Session = Depends(get_db),
):
    """Update candidate."""
    try:
        candidate = CandidateService.update(db, candidate_id, schema)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found",
            )
        return candidate
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{candidate_id}/salary", response_model=CandidateResponse)
def update_candidate_salary(
    candidate_id: UUID,
    schema: CandidateSalaryUpdate,
    db: Session = Depends(get_db),
):
    """Update candidate salary expectations."""
    candidate = CandidateService.update_salary(
        db,
        candidate_id,
        salary_min=schema.salary_min,
        salary_max=schema.salary_max,
        salary_currency=schema.salary_currency,
        salary_type=schema.salary_type,
    )
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(
    candidate_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete candidate."""
    deleted = CandidateService.delete(db, candidate_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )


@router.get("/technology/{technology_id}", response_model=CandidateListResponse)
def get_candidates_by_technology(
    technology_id: UUID,
    db: Session = Depends(get_db),
):
    """Get candidates with experience in a specific technology."""
    candidates = CandidateService.get_by_technology(db, technology_id)

    return {
        "items": candidates,
        "total": len(candidates),
        "page": 1,
        "page_size": len(candidates),
        "total_pages": 1,
    }
