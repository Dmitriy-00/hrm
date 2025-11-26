"""Workplaces (work experience) API endpoints."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas.workplace import (
    WorkplaceCreate,
    WorkplaceUpdate,
    WorkplaceResponse,
    WorkplaceListResponse,
)
from app.services.workplace_service import WorkplaceService

router = APIRouter()


@router.post("/", response_model=WorkplaceResponse, status_code=status.HTTP_201_CREATED)
def create_workplace(
    schema: WorkplaceCreate,
    db: Session = Depends(get_db),
):
    """Create new workplace experience."""
    try:
        workplace = WorkplaceService.create(db, schema)
        return workplace
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/candidate/{candidate_id}", response_model=WorkplaceListResponse)
def get_candidate_workplaces(
    candidate_id: UUID,
    db: Session = Depends(get_db),
):
    """Get all workplaces for a candidate."""
    workplaces = WorkplaceService.get_by_candidate(db, candidate_id)

    return {
        "items": workplaces,
        "total": len(workplaces),
    }


@router.get("/candidate/{candidate_id}/current", response_model=WorkplaceResponse)
def get_current_workplace(
    candidate_id: UUID,
    db: Session = Depends(get_db),
):
    """Get current workplace for a candidate."""
    workplace = WorkplaceService.get_current(db, candidate_id)
    if not workplace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No current workplace found",
        )
    return workplace


@router.get("/candidate/{candidate_id}/statistics")
def get_candidate_workplace_statistics(
    candidate_id: UUID,
    db: Session = Depends(get_db),
):
    """Get workplace statistics for a candidate."""
    stats = WorkplaceService.get_statistics_by_candidate(db, candidate_id)
    return stats


@router.get("/{workplace_id}", response_model=WorkplaceResponse)
def get_workplace(
    workplace_id: UUID,
    db: Session = Depends(get_db),
):
    """Get workplace by ID."""
    workplace = WorkplaceService.get(db, workplace_id)
    if not workplace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workplace not found",
        )
    return workplace


@router.put("/{workplace_id}", response_model=WorkplaceResponse)
def update_workplace(
    workplace_id: UUID,
    schema: WorkplaceUpdate,
    db: Session = Depends(get_db),
):
    """Update workplace."""
    try:
        workplace = WorkplaceService.update(db, workplace_id, schema)
        if not workplace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workplace not found",
            )
        return workplace
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{workplace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workplace(
    workplace_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete workplace."""
    deleted = WorkplaceService.delete(db, workplace_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workplace not found",
        )


@router.post("/{workplace_id}/technologies/{technology_id}")
def add_technology_to_workplace(
    workplace_id: UUID,
    technology_id: UUID,
    proficiency: int = 3,
    usage_intensity: str = "secondary",
    db: Session = Depends(get_db),
):
    """Add technology to workplace."""
    try:
        workplace_tech = WorkplaceService.add_technology(
            db, workplace_id, technology_id, proficiency, usage_intensity
        )
        return {"success": True, "technology_id": str(technology_id)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{workplace_id}/technologies/{technology_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_technology_from_workplace(
    workplace_id: UUID,
    technology_id: UUID,
    db: Session = Depends(get_db),
):
    """Remove technology from workplace."""
    deleted = WorkplaceService.remove_technology(db, workplace_id, technology_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technology not found in this workplace",
        )
