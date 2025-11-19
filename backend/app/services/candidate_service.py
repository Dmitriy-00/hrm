"""Candidate service."""

from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from datetime import datetime

from app.db.models.candidate import Candidate
from app.db.models.workplace import Workplace
from app.models.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateSearchParams


class CandidateService:
    """Service for Candidate operations."""

    @staticmethod
    def create(db: Session, schema: CandidateCreate) -> Candidate:
        """Create new candidate."""
        # Check if email already exists
        existing = db.query(Candidate).filter(Candidate.email == schema.email).first()
        if existing:
            raise ValueError(f"Candidate with email {schema.email} already exists")

        candidate = Candidate(
            user_id=schema.user_id,
            first_name=schema.first_name,
            last_name=schema.last_name,
            email=schema.email,
            phone=schema.phone,
            job_title_id=schema.job_title_id,
            current_job_title=schema.current_job_title,
            grade=schema.grade,
            country=schema.country,
            city=schema.city,
            timezone=schema.timezone,
            citizenship=schema.citizenship,
            relocation=schema.relocation,
            remote_work=schema.remote_work,
            languages=[lang.model_dump() for lang in schema.languages],
            contacts=schema.contacts,
            about_me=schema.about_me,
            status=schema.status,
            available_from=schema.available_from,
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return candidate

    @staticmethod
    def get(db: Session, candidate_id: UUID) -> Optional[Candidate]:
        """Get candidate by ID."""
        return db.query(Candidate).filter(Candidate.id == candidate_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Candidate]:
        """Get candidate by email."""
        return db.query(Candidate).filter(Candidate.email == email).first()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
    ) -> Tuple[List[Candidate], int]:
        """Get all candidates with optional search."""
        query = db.query(Candidate)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Candidate.first_name.ilike(search_pattern),
                    Candidate.last_name.ilike(search_pattern),
                    Candidate.email.ilike(search_pattern),
                    Candidate.current_job_title.ilike(search_pattern),
                )
            )

        total = query.count()
        candidates = query.order_by(Candidate.created_at.desc()).offset(skip).limit(limit).all()

        return candidates, total

    @staticmethod
    def search(
        db: Session,
        params: CandidateSearchParams,
    ) -> Tuple[List[Candidate], int]:
        """Advanced search for candidates."""
        query = db.query(Candidate)

        # Job title filter
        if params.job_title_ids:
            query = query.filter(Candidate.job_title_id.in_(params.job_title_ids))

        # Grade filter
        if params.grades:
            query = query.filter(Candidate.grade.in_(params.grades))

        # Experience filter
        if params.min_experience_years is not None:
            min_months = params.min_experience_years * 12
            query = query.filter(Candidate.experience_months >= min_months)

        if params.max_experience_years is not None:
            max_months = params.max_experience_years * 12
            query = query.filter(Candidate.experience_months <= max_months)

        # Location filters
        if params.countries:
            query = query.filter(Candidate.country.in_(params.countries))

        if params.cities:
            query = query.filter(Candidate.city.in_(params.cities))

        if params.open_to_remote is not None:
            query = query.filter(Candidate.remote_work == params.open_to_remote)

        if params.open_to_relocation is not None:
            query = query.filter(Candidate.relocation == params.open_to_relocation)

        # Salary filter
        if params.salary_min is not None:
            query = query.filter(
                or_(
                    Candidate.salary_min >= params.salary_min,
                    Candidate.salary_min.is_(None),
                )
            )

        if params.salary_max is not None:
            query = query.filter(
                or_(
                    Candidate.salary_max <= params.salary_max,
                    Candidate.salary_max.is_(None),
                )
            )

        # Status filter
        if params.status:
            query = query.filter(Candidate.status.in_(params.status))

        # Text search
        if params.search:
            search_pattern = f"%{params.search}%"
            query = query.filter(
                or_(
                    Candidate.first_name.ilike(search_pattern),
                    Candidate.last_name.ilike(search_pattern),
                    Candidate.current_job_title.ilike(search_pattern),
                    Candidate.about_me.ilike(search_pattern),
                )
            )

        # Get total count before pagination
        total = query.count()

        # Sorting
        if params.sort_by == "experience":
            order_field = Candidate.experience_months
        elif params.sort_by == "last_active":
            order_field = Candidate.last_active
        elif params.sort_by == "salary_min":
            order_field = Candidate.salary_min
        else:
            order_field = Candidate.created_at

        if params.sort_order == "asc":
            query = query.order_by(order_field.asc())
        else:
            query = query.order_by(order_field.desc())

        # Pagination
        skip = (params.page - 1) * params.page_size
        candidates = query.offset(skip).limit(params.page_size).all()

        return candidates, total

    @staticmethod
    def update(db: Session, candidate_id: UUID, schema: CandidateUpdate) -> Optional[Candidate]:
        """Update candidate."""
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return None

        # Check email uniqueness if changing
        if schema.email and schema.email != candidate.email:
            existing = db.query(Candidate).filter(Candidate.email == schema.email).first()
            if existing:
                raise ValueError(f"Candidate with email {schema.email} already exists")

        # Update fields
        update_data = schema.model_dump(exclude_unset=True)

        # Handle languages separately (convert Pydantic models to dicts)
        if "languages" in update_data and update_data["languages"] is not None:
            update_data["languages"] = [lang.model_dump() for lang in schema.languages]

        for field, value in update_data.items():
            setattr(candidate, field, value)

        candidate.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(candidate)

        return candidate

    @staticmethod
    def update_salary(
        db: Session,
        candidate_id: UUID,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        salary_currency: Optional[str] = None,
        salary_type: Optional[str] = None,
    ) -> Optional[Candidate]:
        """Update candidate salary expectations."""
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return None

        if salary_min is not None:
            candidate.salary_min = salary_min
        if salary_max is not None:
            candidate.salary_max = salary_max
        if salary_currency is not None:
            candidate.salary_currency = salary_currency
        if salary_type is not None:
            candidate.salary_type = salary_type

        candidate.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(candidate)

        return candidate

    @staticmethod
    def delete(db: Session, candidate_id: UUID) -> bool:
        """Delete candidate."""
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return False

        db.delete(candidate)
        db.commit()

        return True

    @staticmethod
    def update_experience_months(db: Session, candidate_id: UUID) -> Optional[Candidate]:
        """
        Recalculate and update total experience months based on workplaces.
        Should be called after adding/updating/deleting workplaces.
        """
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return None

        # Get all workplaces for this candidate
        workplaces = db.query(Workplace).filter(Workplace.candidate_id == candidate_id).all()

        # Calculate total months
        total_months = 0
        for workplace in workplaces:
            if workplace.duration_months:
                total_months += workplace.duration_months

        candidate.experience_months = total_months
        db.commit()
        db.refresh(candidate)

        return candidate

    @staticmethod
    def update_last_active(db: Session, candidate_id: UUID) -> Optional[Candidate]:
        """Update last active timestamp."""
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return None

        candidate.last_active = datetime.utcnow()
        db.commit()
        db.refresh(candidate)

        return candidate

    @staticmethod
    def get_by_technology(db: Session, technology_id: UUID) -> List[Candidate]:
        """Get candidates who have experience with a specific technology."""
        from app.db.models.workplace import WorkplaceTechnology

        # Subquery to get candidate IDs with this technology
        subquery = (
            db.query(Workplace.candidate_id)
            .join(WorkplaceTechnology)
            .filter(WorkplaceTechnology.technology_id == technology_id)
            .distinct()
        )

        candidates = db.query(Candidate).filter(Candidate.id.in_(subquery)).all()

        return candidates

    @staticmethod
    def get_statistics(db: Session) -> dict:
        """Get candidate statistics."""
        total = db.query(Candidate).count()

        by_status = (
            db.query(Candidate.status, func.count(Candidate.id))
            .group_by(Candidate.status)
            .all()
        )

        by_grade = (
            db.query(Candidate.grade, func.count(Candidate.id))
            .filter(Candidate.grade.isnot(None))
            .group_by(Candidate.grade)
            .all()
        )

        by_remote = (
            db.query(Candidate.remote_work, func.count(Candidate.id))
            .group_by(Candidate.remote_work)
            .all()
        )

        return {
            "total": total,
            "by_status": {status: count for status, count in by_status},
            "by_grade": {grade: count for grade, count in by_grade},
            "by_remote": {remote: count for remote, count in by_remote},
        }
