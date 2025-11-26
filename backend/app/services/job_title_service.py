"""Job Title service."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models.job_title import JobTitle
from app.models.schemas.job_title import JobTitleCreate, JobTitleUpdate
from app.utils.hierarchy import build_path, calculate_level


class JobTitleService:
    """Service for Job Title operations."""

    @staticmethod
    def create(db: Session, schema: JobTitleCreate) -> JobTitle:
        """Create new job title."""
        # Get parent if exists
        parent = None
        parent_path = None
        if schema.parent_id:
            parent = db.query(JobTitle).filter(JobTitle.id == schema.parent_id).first()
            if not parent:
                raise ValueError(f"Parent job title with id {schema.parent_id} not found")
            parent_path = parent.path

        # Build path and calculate level
        path = build_path(schema.slug, parent_path)
        level = calculate_level(path)

        # Create job title
        job_title = JobTitle(
            name=schema.name,
            slug=schema.slug,
            parent_id=schema.parent_id,
            level=level,
            path=path,
            aliases=schema.aliases,
            description=schema.description,
        )

        db.add(job_title)
        db.commit()
        db.refresh(job_title)

        return job_title

    @staticmethod
    def get(db: Session, job_title_id: UUID) -> Optional[JobTitle]:
        """Get job title by ID."""
        return db.query(JobTitle).filter(JobTitle.id == job_title_id).first()

    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[JobTitle]:
        """Get job title by slug."""
        return db.query(JobTitle).filter(JobTitle.slug == slug).first()

    @staticmethod
    def get_by_path(db: Session, path: str) -> Optional[JobTitle]:
        """Get job title by path."""
        return db.query(JobTitle).filter(JobTitle.path == path).first()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
    ) -> List[JobTitle]:
        """Get all job titles with optional search."""
        query = db.query(JobTitle)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    JobTitle.name.ilike(search_pattern),
                    JobTitle.slug.ilike(search_pattern),
                    JobTitle.path.ilike(search_pattern),
                )
            )

        return query.order_by(JobTitle.path).offset(skip).limit(limit).all()

    @staticmethod
    def get_roots(db: Session) -> List[JobTitle]:
        """Get root job titles (no parent)."""
        return db.query(JobTitle).filter(JobTitle.parent_id.is_(None)).order_by(JobTitle.name).all()

    @staticmethod
    def get_children(db: Session, parent_id: UUID) -> List[JobTitle]:
        """Get direct children of a job title."""
        return db.query(JobTitle).filter(JobTitle.parent_id == parent_id).order_by(JobTitle.name).all()

    @staticmethod
    def get_descendants(db: Session, path: str) -> List[JobTitle]:
        """Get all descendants of a job title."""
        return db.query(JobTitle).filter(JobTitle.path.like(f"{path}.%")).order_by(JobTitle.path).all()

    @staticmethod
    def update(db: Session, job_title_id: UUID, schema: JobTitleUpdate) -> Optional[JobTitle]:
        """Update job title."""
        job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
        if not job_title:
            return None

        # Update fields
        update_data = schema.model_dump(exclude_unset=True)

        # If parent_id or slug changed, recalculate path and level
        if "parent_id" in update_data or "slug" in update_data:
            parent_path = None
            if update_data.get("parent_id"):
                parent = db.query(JobTitle).filter(JobTitle.id == update_data["parent_id"]).first()
                if not parent:
                    raise ValueError(f"Parent job title not found")
                parent_path = parent.path

            slug = update_data.get("slug", job_title.slug)
            path = build_path(slug, parent_path)
            level = calculate_level(path)

            update_data["path"] = path
            update_data["level"] = level

        for field, value in update_data.items():
            setattr(job_title, field, value)

        db.commit()
        db.refresh(job_title)

        return job_title

    @staticmethod
    def delete(db: Session, job_title_id: UUID) -> bool:
        """Delete job title."""
        job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
        if not job_title:
            return False

        # Check if has children
        children_count = db.query(JobTitle).filter(JobTitle.parent_id == job_title_id).count()
        if children_count > 0:
            raise ValueError("Cannot delete job title with children")

        db.delete(job_title)
        db.commit()

        return True

    @staticmethod
    def search_by_alias(db: Session, alias: str) -> List[JobTitle]:
        """Search job titles by alias."""
        return db.query(JobTitle).filter(JobTitle.aliases.contains([alias])).all()
