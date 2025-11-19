"""Industries API endpoints."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas.industry import (
    IndustryCreate,
    IndustryUpdate,
    IndustryResponse,
    IndustryTree,
)
from app.services.industry_service import IndustryService
from app.utils.hierarchy import build_tree

router = APIRouter()


@router.post("/", response_model=IndustryResponse, status_code=status.HTTP_201_CREATED)
def create_industry(
    schema: IndustryCreate,
    db: Session = Depends(get_db),
):
    """Create new industry."""
    industry = IndustryService.create(db, schema)
    return industry


@router.get("/", response_model=List[IndustryResponse])
def get_industries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all industries with optional search."""
    industries = IndustryService.get_all(db, skip=skip, limit=limit, search=search)
    return industries


@router.get("/roots", response_model=List[IndustryResponse])
def get_root_industries(db: Session = Depends(get_db)):
    """Get root industries (no parent)."""
    return IndustryService.get_roots(db)


@router.get("/tree", response_model=List[IndustryTree])
def get_industry_tree(db: Session = Depends(get_db)):
    """Get industries as tree structure."""
    all_industries = IndustryService.get_all(db, skip=0, limit=10000)
    tree = build_tree(all_industries)
    return tree


@router.get("/{industry_id}", response_model=IndustryResponse)
def get_industry(
    industry_id: UUID,
    db: Session = Depends(get_db),
):
    """Get industry by ID."""
    industry = IndustryService.get(db, industry_id)
    if not industry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found",
        )
    return industry


@router.get("/path/{path:path}", response_model=IndustryResponse)
def get_industry_by_path(
    path: str,
    db: Session = Depends(get_db),
):
    """Get industry by path."""
    industry = IndustryService.get_by_path(db, path)
    if not industry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found",
        )
    return industry


@router.get("/{industry_id}/children", response_model=List[IndustryResponse])
def get_industry_children(
    industry_id: UUID,
    db: Session = Depends(get_db),
):
    """Get direct children of an industry."""
    # Check if parent exists
    parent = IndustryService.get(db, industry_id)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found",
        )

    return IndustryService.get_children(db, industry_id)


@router.put("/{industry_id}", response_model=IndustryResponse)
def update_industry(
    industry_id: UUID,
    schema: IndustryUpdate,
    db: Session = Depends(get_db),
):
    """Update industry."""
    industry = IndustryService.update(db, industry_id, schema)
    if not industry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Industry not found",
        )
    return industry


@router.delete("/{industry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_industry(
    industry_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete industry."""
    try:
        deleted = IndustryService.delete(db, industry_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Industry not found",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
