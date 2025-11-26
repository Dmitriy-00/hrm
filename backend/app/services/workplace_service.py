"""Workplace (work experience) service."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from app.db.models.workplace import Workplace, WorkplaceTechnology
from app.models.schemas.workplace import WorkplaceCreate, WorkplaceUpdate


class WorkplaceService:
    """Service for Workplace operations."""

    @staticmethod
    def _calculate_duration_months(start_date: date, end_date: Optional[date] = None) -> int:
        """Calculate duration in months between two dates."""
        if end_date is None:
            end_date = date.today()

        delta = relativedelta(end_date, start_date)
        return delta.years * 12 + delta.months

    @staticmethod
    def create(db: Session, schema: WorkplaceCreate) -> Workplace:
        """Create new workplace experience."""
        # Calculate duration
        duration_months = WorkplaceService._calculate_duration_months(
            schema.start_date, schema.end_date
        )

        workplace = Workplace(
            candidate_id=schema.candidate_id,
            company_name=schema.company_name,
            company_id=schema.company_id,
            industry_ids=schema.industry_ids,
            company_size=schema.company_size,
            job_title_id=schema.job_title_id,
            position_name=schema.position_name,
            grade=schema.grade,
            start_date=schema.start_date,
            end_date=schema.end_date,
            duration_months=duration_months,
            description=schema.description,
            achievements=schema.achievements,
            skills=[skill.model_dump() for skill in schema.skills],
            standards_used=[std.model_dump() for std in schema.standards_used],
            project_types=schema.project_types,
            team_size=schema.team_size,
            role=schema.role,
        )

        db.add(workplace)
        db.flush()  # Get workplace ID

        # Add technologies
        for tech_data in schema.technologies:
            workplace_tech = WorkplaceTechnology(
                workplace_id=workplace.id,
                technology_id=tech_data.technology_id,
                proficiency=tech_data.proficiency,
                usage_intensity=tech_data.usage_intensity,
            )
            db.add(workplace_tech)

        db.commit()
        db.refresh(workplace)

        # Update candidate's total experience
        from app.services.candidate_service import CandidateService
        CandidateService.update_experience_months(db, schema.candidate_id)

        return workplace

    @staticmethod
    def get(db: Session, workplace_id: UUID) -> Optional[Workplace]:
        """Get workplace by ID."""
        return db.query(Workplace).filter(Workplace.id == workplace_id).first()

    @staticmethod
    def get_by_candidate(db: Session, candidate_id: UUID) -> List[Workplace]:
        """Get all workplaces for a candidate."""
        return (
            db.query(Workplace)
            .filter(Workplace.candidate_id == candidate_id)
            .order_by(Workplace.start_date.desc())
            .all()
        )

    @staticmethod
    def get_current(db: Session, candidate_id: UUID) -> Optional[Workplace]:
        """Get current workplace for a candidate (end_date is None)."""
        return (
            db.query(Workplace)
            .filter(
                Workplace.candidate_id == candidate_id,
                Workplace.end_date.is_(None),
            )
            .first()
        )

    @staticmethod
    def update(db: Session, workplace_id: UUID, schema: WorkplaceUpdate) -> Optional[Workplace]:
        """Update workplace."""
        workplace = db.query(Workplace).filter(Workplace.id == workplace_id).first()
        if not workplace:
            return None

        update_data = schema.model_dump(exclude_unset=True)

        # Recalculate duration if dates changed
        if "start_date" in update_data or "end_date" in update_data:
            start_date = update_data.get("start_date", workplace.start_date)
            end_date = update_data.get("end_date", workplace.end_date)
            duration_months = WorkplaceService._calculate_duration_months(start_date, end_date)
            update_data["duration_months"] = duration_months

        # Handle skills and standards_used separately
        if "skills" in update_data and update_data["skills"] is not None:
            update_data["skills"] = [skill.model_dump() for skill in schema.skills]

        if "standards_used" in update_data and update_data["standards_used"] is not None:
            update_data["standards_used"] = [std.model_dump() for std in schema.standards_used]

        # Update technologies if provided
        if "technologies" in update_data and update_data["technologies"] is not None:
            # Delete existing technologies
            db.query(WorkplaceTechnology).filter(
                WorkplaceTechnology.workplace_id == workplace_id
            ).delete()

            # Add new technologies
            for tech_data in schema.technologies:
                workplace_tech = WorkplaceTechnology(
                    workplace_id=workplace_id,
                    technology_id=tech_data.technology_id,
                    proficiency=tech_data.proficiency,
                    usage_intensity=tech_data.usage_intensity,
                )
                db.add(workplace_tech)

            del update_data["technologies"]

        # Update other fields
        for field, value in update_data.items():
            setattr(workplace, field, value)

        workplace.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(workplace)

        # Update candidate's total experience
        from app.services.candidate_service import CandidateService
        CandidateService.update_experience_months(db, workplace.candidate_id)

        return workplace

    @staticmethod
    def delete(db: Session, workplace_id: UUID) -> bool:
        """Delete workplace."""
        workplace = db.query(Workplace).filter(Workplace.id == workplace_id).first()
        if not workplace:
            return False

        candidate_id = workplace.candidate_id

        db.delete(workplace)
        db.commit()

        # Update candidate's total experience
        from app.services.candidate_service import CandidateService
        CandidateService.update_experience_months(db, candidate_id)

        return True

    @staticmethod
    def get_technologies(db: Session, workplace_id: UUID) -> List[WorkplaceTechnology]:
        """Get all technologies for a workplace."""
        return (
            db.query(WorkplaceTechnology)
            .filter(WorkplaceTechnology.workplace_id == workplace_id)
            .all()
        )

    @staticmethod
    def add_technology(
        db: Session,
        workplace_id: UUID,
        technology_id: UUID,
        proficiency: int = 3,
        usage_intensity: str = "secondary",
    ) -> WorkplaceTechnology:
        """Add technology to workplace."""
        # Check if already exists
        existing = (
            db.query(WorkplaceTechnology)
            .filter(
                WorkplaceTechnology.workplace_id == workplace_id,
                WorkplaceTechnology.technology_id == technology_id,
            )
            .first()
        )

        if existing:
            # Update existing
            existing.proficiency = proficiency
            existing.usage_intensity = usage_intensity
            db.commit()
            db.refresh(existing)
            return existing

        # Create new
        workplace_tech = WorkplaceTechnology(
            workplace_id=workplace_id,
            technology_id=technology_id,
            proficiency=proficiency,
            usage_intensity=usage_intensity,
        )

        db.add(workplace_tech)
        db.commit()
        db.refresh(workplace_tech)

        return workplace_tech

    @staticmethod
    def remove_technology(db: Session, workplace_id: UUID, technology_id: UUID) -> bool:
        """Remove technology from workplace."""
        result = (
            db.query(WorkplaceTechnology)
            .filter(
                WorkplaceTechnology.workplace_id == workplace_id,
                WorkplaceTechnology.technology_id == technology_id,
            )
            .delete()
        )

        db.commit()

        return result > 0

    @staticmethod
    def get_statistics_by_candidate(db: Session, candidate_id: UUID) -> dict:
        """Get workplace statistics for a candidate."""
        workplaces = WorkplaceService.get_by_candidate(db, candidate_id)

        total_months = sum(w.duration_months or 0 for w in workplaces)
        total_companies = len(workplaces)

        # Get all unique technologies
        all_technologies = set()
        for workplace in workplaces:
            for tech in workplace.technologies:
                all_technologies.add(tech.technology_id)

        # Get industries
        all_industries = set()
        for workplace in workplaces:
            all_industries.update(workplace.industry_ids)

        # Latest position
        latest_workplace = workplaces[0] if workplaces else None

        return {
            "total_months": total_months,
            "total_years": round(total_months / 12, 1),
            "total_companies": total_companies,
            "unique_technologies": len(all_technologies),
            "unique_industries": len(all_industries),
            "current_position": latest_workplace.position_name if latest_workplace and not latest_workplace.end_date else None,
            "current_company": latest_workplace.company_name if latest_workplace and not latest_workplace.end_date else None,
        }
