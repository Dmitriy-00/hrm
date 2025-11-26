"""Vacancy service."""

from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from datetime import datetime

from app.db.models.vacancy import Vacancy
from app.db.models.vacancy_requirement import VacancyRequirement
from app.models.schemas.vacancy import (
    VacancyCreate,
    VacancyUpdate,
    VacancySearchParams,
    VacancyRequirementSchema,
)


class VacancyService:
    """Service for Vacancy operations."""

    @staticmethod
    def create(db: Session, schema: VacancyCreate) -> Vacancy:
        """Create new vacancy."""
        vacancy = Vacancy(
            company_id=schema.company_id,
            company_name=schema.company_name,
            job_title_id=schema.job_title_id,
            position_name=schema.position_name,
            grade=schema.grade,
            min_experience_years=schema.min_experience_years,
            max_experience_years=schema.max_experience_years,
            locations=[loc.model_dump() for loc in schema.locations],
            timezone_requirements=schema.timezone_requirements,
            language_requirements=[lang.model_dump() for lang in schema.language_requirements],
            citizenship_allowed=schema.citizenship_allowed,
            citizenship_restricted=schema.citizenship_restricted,
            salary_min=schema.salary_min,
            salary_max=schema.salary_max,
            salary_currency=schema.salary_currency,
            salary_type=schema.salary_type,
            salary_period=schema.salary_period,
            salary_negotiable=schema.salary_negotiable,
            status=schema.status,
            deadline=schema.deadline,
            description=schema.description,
            responsibilities=schema.responsibilities,
            interview_process=schema.interview_process,
            external_links=schema.external_links,
            created_by=schema.created_by,
        )

        db.add(vacancy)
        db.flush()  # Get vacancy ID

        # Add requirements
        for req_data in schema.requirements:
            requirement = VacancyRequirement(
                vacancy_id=vacancy.id,
                technology_id=req_data.technology_id,
                importance=req_data.importance,
                min_experience_years=req_data.min_experience_years,
                proficiency_level=req_data.proficiency_level,
            )
            db.add(requirement)

        db.commit()
        db.refresh(vacancy)

        return vacancy

    @staticmethod
    def get(db: Session, vacancy_id: UUID) -> Optional[Vacancy]:
        """Get vacancy by ID."""
        return db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Tuple[List[Vacancy], int]:
        """Get all vacancies with optional search and status filter."""
        query = db.query(Vacancy)

        if status:
            query = query.filter(Vacancy.status == status)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Vacancy.position_name.ilike(search_pattern),
                    Vacancy.company_name.ilike(search_pattern),
                    Vacancy.description.ilike(search_pattern),
                )
            )

        total = query.count()
        vacancies = query.order_by(Vacancy.created_at.desc()).offset(skip).limit(limit).all()

        return vacancies, total

    @staticmethod
    def search(
        db: Session,
        params: VacancySearchParams,
    ) -> Tuple[List[Vacancy], int]:
        """Advanced search for vacancies."""
        query = db.query(Vacancy)

        # Job title filter
        if params.job_title_ids:
            query = query.filter(Vacancy.job_title_id.in_(params.job_title_ids))

        # Grade filter
        if params.grades:
            query = query.filter(Vacancy.grade.in_(params.grades))

        # Experience filter
        if params.min_experience_years is not None:
            query = query.filter(
                or_(
                    Vacancy.min_experience_years <= params.min_experience_years,
                    Vacancy.min_experience_years.is_(None),
                )
            )

        if params.max_experience_years is not None:
            query = query.filter(
                or_(
                    Vacancy.max_experience_years >= params.max_experience_years,
                    Vacancy.max_experience_years.is_(None),
                )
            )

        # Company filter
        if params.company_ids:
            query = query.filter(Vacancy.company_id.in_(params.company_ids))

        # Salary filter
        if params.salary_min is not None:
            query = query.filter(
                or_(
                    Vacancy.salary_max >= params.salary_min,
                    Vacancy.salary_max.is_(None),
                    Vacancy.salary_negotiable == True,
                )
            )

        if params.salary_max is not None:
            query = query.filter(
                or_(
                    Vacancy.salary_min <= params.salary_max,
                    Vacancy.salary_min.is_(None),
                    Vacancy.salary_negotiable == True,
                )
            )

        # Status filter
        if params.status:
            query = query.filter(Vacancy.status.in_(params.status))

        # Text search
        if params.search:
            search_pattern = f"%{params.search}%"
            query = query.filter(
                or_(
                    Vacancy.position_name.ilike(search_pattern),
                    Vacancy.company_name.ilike(search_pattern),
                    Vacancy.description.ilike(search_pattern),
                )
            )

        # Get total count before pagination
        total = query.count()

        # Sorting
        if params.sort_by == "salary_min":
            order_field = Vacancy.salary_min
        elif params.sort_by == "deadline":
            order_field = Vacancy.deadline
        else:
            order_field = Vacancy.created_at

        if params.sort_order == "asc":
            query = query.order_by(order_field.asc().nullslast())
        else:
            query = query.order_by(order_field.desc().nullslast())

        # Pagination
        skip = (params.page - 1) * params.page_size
        vacancies = query.offset(skip).limit(params.page_size).all()

        return vacancies, total

    @staticmethod
    def update(db: Session, vacancy_id: UUID, schema: VacancyUpdate) -> Optional[Vacancy]:
        """Update vacancy."""
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            return None

        update_data = schema.model_dump(exclude_unset=True)

        # Handle nested objects
        if "locations" in update_data and update_data["locations"] is not None:
            update_data["locations"] = [loc.model_dump() for loc in schema.locations]

        if "language_requirements" in update_data and update_data["language_requirements"] is not None:
            update_data["language_requirements"] = [lang.model_dump() for lang in schema.language_requirements]

        for field, value in update_data.items():
            setattr(vacancy, field, value)

        vacancy.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(vacancy)

        return vacancy

    @staticmethod
    def update_requirements(
        db: Session,
        vacancy_id: UUID,
        requirements: List[VacancyRequirementSchema],
    ) -> Optional[Vacancy]:
        """Update vacancy requirements (replace all)."""
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            return None

        # Delete existing requirements
        db.query(VacancyRequirement).filter(
            VacancyRequirement.vacancy_id == vacancy_id
        ).delete()

        # Add new requirements
        for req_data in requirements:
            requirement = VacancyRequirement(
                vacancy_id=vacancy_id,
                technology_id=req_data.technology_id,
                importance=req_data.importance,
                min_experience_years=req_data.min_experience_years,
                proficiency_level=req_data.proficiency_level,
            )
            db.add(requirement)

        db.commit()
        db.refresh(vacancy)

        return vacancy

    @staticmethod
    def delete(db: Session, vacancy_id: UUID) -> bool:
        """Delete vacancy."""
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            return False

        db.delete(vacancy)
        db.commit()

        return True

    @staticmethod
    def get_by_company(db: Session, company_id: UUID) -> List[Vacancy]:
        """Get all vacancies for a company."""
        return (
            db.query(Vacancy)
            .filter(Vacancy.company_id == company_id)
            .order_by(Vacancy.created_at.desc())
            .all()
        )

    @staticmethod
    def get_active(db: Session, limit: int = 100) -> List[Vacancy]:
        """Get active vacancies."""
        return (
            db.query(Vacancy)
            .filter(Vacancy.status == "active")
            .order_by(Vacancy.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_technology(db: Session, technology_id: UUID) -> List[Vacancy]:
        """Get vacancies requiring a specific technology."""
        # Subquery to get vacancy IDs with this technology
        subquery = (
            db.query(VacancyRequirement.vacancy_id)
            .filter(VacancyRequirement.technology_id == technology_id)
            .distinct()
        )

        vacancies = db.query(Vacancy).filter(Vacancy.id.in_(subquery)).all()

        return vacancies

    @staticmethod
    def get_requirements(db: Session, vacancy_id: UUID) -> List[VacancyRequirement]:
        """Get all requirements for a vacancy."""
        return (
            db.query(VacancyRequirement)
            .filter(VacancyRequirement.vacancy_id == vacancy_id)
            .all()
        )

    @staticmethod
    def add_requirement(
        db: Session,
        vacancy_id: UUID,
        technology_id: UUID,
        importance: str = "required",
        min_experience_years: Optional[int] = None,
        proficiency_level: int = 3,
    ) -> VacancyRequirement:
        """Add requirement to vacancy."""
        # Check if already exists
        existing = (
            db.query(VacancyRequirement)
            .filter(
                VacancyRequirement.vacancy_id == vacancy_id,
                VacancyRequirement.technology_id == technology_id,
            )
            .first()
        )

        if existing:
            # Update existing
            existing.importance = importance
            existing.min_experience_years = min_experience_years
            existing.proficiency_level = proficiency_level
            db.commit()
            db.refresh(existing)
            return existing

        # Create new
        requirement = VacancyRequirement(
            vacancy_id=vacancy_id,
            technology_id=technology_id,
            importance=importance,
            min_experience_years=min_experience_years,
            proficiency_level=proficiency_level,
        )

        db.add(requirement)
        db.commit()
        db.refresh(requirement)

        return requirement

    @staticmethod
    def remove_requirement(db: Session, vacancy_id: UUID, technology_id: UUID) -> bool:
        """Remove requirement from vacancy."""
        result = (
            db.query(VacancyRequirement)
            .filter(
                VacancyRequirement.vacancy_id == vacancy_id,
                VacancyRequirement.technology_id == technology_id,
            )
            .delete()
        )

        db.commit()

        return result > 0

    @staticmethod
    def get_statistics(db: Session) -> dict:
        """Get vacancy statistics."""
        total = db.query(Vacancy).count()

        by_status = (
            db.query(Vacancy.status, func.count(Vacancy.id))
            .group_by(Vacancy.status)
            .all()
        )

        by_grade = (
            db.query(Vacancy.grade, func.count(Vacancy.id))
            .filter(Vacancy.grade.isnot(None))
            .group_by(Vacancy.grade)
            .all()
        )

        active_count = db.query(Vacancy).filter(Vacancy.status == "active").count()

        return {
            "total": total,
            "active": active_count,
            "by_status": {status: count for status, count in by_status},
            "by_grade": {grade: count for grade, count in by_grade},
        }
