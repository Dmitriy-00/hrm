"""Standards API endpoints."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas.standard import (
    StandardCreate,
    StandardUpdate,
    StandardResponse,
)
from app.services.standard_service import StandardService

router = APIRouter()


@router.post("/", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
def create_standard(
    schema: StandardCreate,
    db: Session = Depends(get_db),
):
    """Create new standard."""
    standard = StandardService.create(db, schema)
    return standard


@router.get("/", response_model=List[StandardResponse])
def get_standards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all standards with optional filters."""
    standards = StandardService.get_all(
        db, skip=skip, limit=limit, type=type, category=category, search=search
    )
    return standards


@router.get("/type/{standard_type}", response_model=List[StandardResponse])
def get_standards_by_type(
    standard_type: str,
    db: Session = Depends(get_db),
):
    """Get standards by type."""
    return StandardService.get_by_type(db, standard_type)


@router.get("/category/{category}", response_model=List[StandardResponse])
def get_standards_by_category(
    category: str,
    db: Session = Depends(get_db),
):
    """Get standards by category."""
    return StandardService.get_by_category(db, category)


@router.get("/job-title/{job_title_id}", response_model=List[StandardResponse])
def get_standards_for_job_title(
    job_title_id: UUID,
    db: Session = Depends(get_db),
):
    """Get standards applicable to a job title."""
    return StandardService.get_for_job_title(db, job_title_id)


@router.get("/{standard_id}", response_model=StandardResponse)
def get_standard(
    standard_id: UUID,
    db: Session = Depends(get_db),
):
    """Get standard by ID."""
    standard = StandardService.get(db, standard_id)
    if not standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found",
        )
    return standard


@router.put("/{standard_id}", response_model=StandardResponse)
def update_standard(
    standard_id: UUID,
    schema: StandardUpdate,
    db: Session = Depends(get_db),
):
    """Update standard."""
    standard = StandardService.update(db, standard_id, schema)
    if not standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found",
        )
    return standard


@router.delete("/{standard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_standard(
    standard_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete standard."""
    deleted = StandardService.delete(db, standard_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Standard not found",
        )
