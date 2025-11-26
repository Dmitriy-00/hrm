"""Job Titles API endpoints."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas.job_title import (
    JobTitleCreate,
    JobTitleUpdate,
    JobTitleResponse,
    JobTitleTree,
)
from app.services.job_title_service import JobTitleService
from app.utils.hierarchy import build_tree

router = APIRouter()


@router.post("/", response_model=JobTitleResponse, status_code=status.HTTP_201_CREATED)
def create_job_title(
    schema: JobTitleCreate,
    db: Session = Depends(get_db),
):
    """Create new job title."""
    try:
        # Check if slug already exists
        existing = JobTitleService.get_by_slug(db, schema.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job title with slug '{schema.slug}' already exists",
            )

        job_title = JobTitleService.create(db, schema)
        return job_title
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[JobTitleResponse])
def get_job_titles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all job titles with optional search."""
    job_titles = JobTitleService.get_all(db, skip=skip, limit=limit, search=search)
    return job_titles


@router.get("/roots", response_model=List[JobTitleResponse])
def get_root_job_titles(db: Session = Depends(get_db)):
    """Get root job titles (no parent)."""
    return JobTitleService.get_roots(db)


@router.get("/tree", response_model=List[JobTitleTree])
def get_job_title_tree(db: Session = Depends(get_db)):
    """Get job titles as tree structure."""
    all_job_titles = JobTitleService.get_all(db, skip=0, limit=10000)
    tree = build_tree(all_job_titles)
    return tree


@router.get("/{job_title_id}", response_model=JobTitleResponse)
def get_job_title(
    job_title_id: UUID,
    db: Session = Depends(get_db),
):
    """Get job title by ID."""
    job_title = JobTitleService.get(db, job_title_id)
    if not job_title:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job title not found",
        )
    return job_title


@router.get("/slug/{slug}", response_model=JobTitleResponse)
def get_job_title_by_slug(
    slug: str,
    db: Session = Depends(get_db),
):
    """Get job title by slug."""
    job_title = JobTitleService.get_by_slug(db, slug)
    if not job_title:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job title not found",
        )
    return job_title


@router.get("/path/{path:path}", response_model=JobTitleResponse)
def get_job_title_by_path(
    path: str,
    db: Session = Depends(get_db),
):
    """Get job title by path."""
    job_title = JobTitleService.get_by_path(db, path)
    if not job_title:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job title not found",
        )
    return job_title


@router.get("/{job_title_id}/children", response_model=List[JobTitleResponse])
def get_job_title_children(
    job_title_id: UUID,
    db: Session = Depends(get_db),
):
    """Get direct children of a job title."""
    # Check if parent exists
    parent = JobTitleService.get(db, job_title_id)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job title not found",
        )

    return JobTitleService.get_children(db, job_title_id)


@router.put("/{job_title_id}", response_model=JobTitleResponse)
def update_job_title(
    job_title_id: UUID,
    schema: JobTitleUpdate,
    db: Session = Depends(get_db),
):
    """Update job title."""
    try:
        job_title = JobTitleService.update(db, job_title_id, schema)
        if not job_title:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job title not found",
            )
        return job_title
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{job_title_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_title(
    job_title_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete job title."""
    try:
        deleted = JobTitleService.delete(db, job_title_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job title not found",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
