"""Technologies API endpoints."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas.technology import (
    TechnologyCreate,
    TechnologyUpdate,
    TechnologyResponse,
    TechnologyTree,
)
from app.services.technology_service import TechnologyService
from app.utils.hierarchy import build_tree

router = APIRouter()


@router.post("/", response_model=TechnologyResponse, status_code=status.HTTP_201_CREATED)
def create_technology(
    schema: TechnologyCreate,
    db: Session = Depends(get_db),
):
    """Create new technology."""
    try:
        # Check if slug already exists
        existing = TechnologyService.get_by_slug(db, schema.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Technology with slug '{schema.slug}' already exists",
            )

        technology = TechnologyService.create(db, schema)
        return technology
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[TechnologyResponse])
def get_technologies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all technologies with optional filters."""
    technologies = TechnologyService.get_all(
        db, skip=skip, limit=limit, category=category, search=search
    )
    return technologies


@router.get("/popular", response_model=List[TechnologyResponse])
def get_popular_technologies(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get most popular technologies."""
    return TechnologyService.get_popular(db, limit=limit)


@router.get("/category/{category}", response_model=List[TechnologyResponse])
def get_technologies_by_category(
    category: str,
    db: Session = Depends(get_db),
):
    """Get technologies by category."""
    return TechnologyService.get_by_category(db, category)


@router.get("/tree", response_model=List[TechnologyTree])
def get_technology_tree(db: Session = Depends(get_db)):
    """Get technologies as tree structure."""
    all_technologies = TechnologyService.get_all(db, skip=0, limit=10000)
    tree = build_tree(all_technologies)
    return tree


@router.get("/{technology_id}", response_model=TechnologyResponse)
def get_technology(
    technology_id: UUID,
    db: Session = Depends(get_db),
):
    """Get technology by ID."""
    technology = TechnologyService.get(db, technology_id)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technology not found",
        )
    return technology


@router.get("/slug/{slug}", response_model=TechnologyResponse)
def get_technology_by_slug(
    slug: str,
    db: Session = Depends(get_db),
):
    """Get technology by slug."""
    technology = TechnologyService.get_by_slug(db, slug)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technology not found",
        )
    return technology


@router.get("/{technology_id}/related", response_model=List[TechnologyResponse])
def get_related_technologies(
    technology_id: UUID,
    db: Session = Depends(get_db),
):
    """Get related technologies."""
    # Check if technology exists
    technology = TechnologyService.get(db, technology_id)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technology not found",
        )

    return TechnologyService.get_related(db, technology_id)


@router.put("/{technology_id}", response_model=TechnologyResponse)
def update_technology(
    technology_id: UUID,
    schema: TechnologyUpdate,
    db: Session = Depends(get_db),
):
    """Update technology."""
    try:
        technology = TechnologyService.update(db, technology_id, schema)
        if not technology:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Technology not found",
            )
        return technology
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{technology_id}/popularity", response_model=TechnologyResponse)
def update_technology_popularity(
    technology_id: UUID,
    score: int = Query(..., ge=0, le=100),
    db: Session = Depends(get_db),
):
    """Update technology popularity score."""
    technology = TechnologyService.update_popularity(db, technology_id, score)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technology not found",
        )
    return technology


@router.delete("/{technology_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technology(
    technology_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete technology."""
    deleted = TechnologyService.delete(db, technology_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technology not found",
        )
