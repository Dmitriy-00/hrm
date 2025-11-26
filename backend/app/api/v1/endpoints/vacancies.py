"""Vacancies API endpoints."""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from math import ceil

from app.db.database import get_db
from app.models.schemas.vacancy import (
    VacancyCreate,
    VacancyUpdate,
    VacancyResponse,
    VacancyListResponse,
    VacancySearchParams,
    VacancyRequirementsUpdate,
)
from app.services.vacancy_service import VacancyService

router = APIRouter()


@router.post("/", response_model=VacancyResponse, status_code=status.HTTP_201_CREATED)
def create_vacancy(
    schema: VacancyCreate,
    db: Session = Depends(get_db),
):
    """Create new vacancy."""
    try:
        vacancy = VacancyService.create(db, schema)
        return vacancy
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=VacancyListResponse)
def get_vacancies(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all vacancies with optional search and status filter."""
    vacancies, total = VacancyService.get_all(
        db, skip=skip, limit=limit, search=search, status=status
    )

    return {
        "items": vacancies,
        "total": total,
        "page": (skip // limit) + 1,
        "page_size": limit,
        "total_pages": ceil(total / limit) if total > 0 else 0,
    }


@router.post("/search", response_model=VacancyListResponse)
def search_vacancies(
    params: VacancySearchParams,
    db: Session = Depends(get_db),
):
    """Advanced search for vacancies."""
    vacancies, total = VacancyService.search(db, params)

    return {
        "items": vacancies,
        "total": total,
        "page": params.page,
        "page_size": params.page_size,
        "total_pages": ceil(total / params.page_size) if total > 0 else 0,
    }


@router.get("/active", response_model=VacancyListResponse)
def get_active_vacancies(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Get active vacancies."""
    vacancies = VacancyService.get_active(db, limit=limit)

    return {
        "items": vacancies,
        "total": len(vacancies),
        "page": 1,
        "page_size": len(vacancies),
        "total_pages": 1,
    }


@router.get("/statistics")
def get_vacancy_statistics(db: Session = Depends(get_db)):
    """Get vacancy statistics."""
    stats = VacancyService.get_statistics(db)
    return stats


@router.get("/{vacancy_id}", response_model=VacancyResponse)
def get_vacancy(
    vacancy_id: UUID,
    db: Session = Depends(get_db),
):
    """Get vacancy by ID."""
    vacancy = VacancyService.get(db, vacancy_id)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )
    return vacancy


@router.put("/{vacancy_id}", response_model=VacancyResponse)
def update_vacancy(
    vacancy_id: UUID,
    schema: VacancyUpdate,
    db: Session = Depends(get_db),
):
    """Update vacancy."""
    try:
        vacancy = VacancyService.update(db, vacancy_id, schema)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vacancy not found",
            )
        return vacancy
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{vacancy_id}/requirements", response_model=VacancyResponse)
def update_vacancy_requirements(
    vacancy_id: UUID,
    schema: VacancyRequirementsUpdate,
    db: Session = Depends(get_db),
):
    """Update vacancy requirements (replace all)."""
    vacancy = VacancyService.update_requirements(db, vacancy_id, schema.requirements)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )
    return vacancy


@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacancy(
    vacancy_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete vacancy."""
    deleted = VacancyService.delete(db, vacancy_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )


@router.get("/company/{company_id}", response_model=VacancyListResponse)
def get_company_vacancies(
    company_id: UUID,
    db: Session = Depends(get_db),
):
    """Get all vacancies for a company."""
    vacancies = VacancyService.get_by_company(db, company_id)

    return {
        "items": vacancies,
        "total": len(vacancies),
        "page": 1,
        "page_size": len(vacancies),
        "total_pages": 1,
    }


@router.get("/technology/{technology_id}", response_model=VacancyListResponse)
def get_vacancies_by_technology(
    technology_id: UUID,
    db: Session = Depends(get_db),
):
    """Get vacancies requiring a specific technology."""
    vacancies = VacancyService.get_by_technology(db, technology_id)

    return {
        "items": vacancies,
        "total": len(vacancies),
        "page": 1,
        "page_size": len(vacancies),
        "total_pages": 1,
    }


@router.post("/{vacancy_id}/requirements/{technology_id}")
def add_requirement_to_vacancy(
    vacancy_id: UUID,
    technology_id: UUID,
    importance: str = Query("required", pattern="^(required|nice_to_have|plus)$"),
    min_experience_years: Optional[int] = Query(None, ge=0),
    proficiency_level: int = Query(3, ge=1, le=5),
    db: Session = Depends(get_db),
):
    """Add technology requirement to vacancy."""
    try:
        requirement = VacancyService.add_requirement(
            db,
            vacancy_id,
            technology_id,
            importance,
            min_experience_years,
            proficiency_level,
        )
        return {"success": True, "technology_id": str(technology_id)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{vacancy_id}/requirements/{technology_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_requirement_from_vacancy(
    vacancy_id: UUID,
    technology_id: UUID,
    db: Session = Depends(get_db),
):
    """Remove technology requirement from vacancy."""
    deleted = VacancyService.remove_requirement(db, vacancy_id, technology_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found",
        )
