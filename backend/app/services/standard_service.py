"""Standard service."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models.standard import Standard
from app.models.schemas.standard import StandardCreate, StandardUpdate


class StandardService:
    """Service for Standard operations."""

    @staticmethod
    def create(db: Session, schema: StandardCreate) -> Standard:
        """Create new standard."""
        standard = Standard(
            name=schema.name,
            type=schema.type,
            category=schema.category,
            path=schema.path,
            description=schema.description,
            applicable_to=schema.applicable_to,
            related_tools=schema.related_tools,
            difficulty=schema.difficulty,
            importance_by_grade=schema.importance_by_grade,
        )

        db.add(standard)
        db.commit()
        db.refresh(standard)

        return standard

    @staticmethod
    def get(db: Session, standard_id: UUID) -> Optional[Standard]:
        """Get standard by ID."""
        return db.query(Standard).filter(Standard.id == standard_id).first()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        type: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Standard]:
        """Get all standards with optional filters."""
        query = db.query(Standard)

        if type:
            query = query.filter(Standard.type == type)

        if category:
            query = query.filter(Standard.category == category)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Standard.name.ilike(search_pattern),
                    Standard.category.ilike(search_pattern),
                )
            )

        return query.order_by(Standard.name).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_type(db: Session, standard_type: str) -> List[Standard]:
        """Get standards by type."""
        return db.query(Standard).filter(Standard.type == standard_type).order_by(Standard.name).all()

    @staticmethod
    def get_by_category(db: Session, category: str) -> List[Standard]:
        """Get standards by category."""
        return db.query(Standard).filter(Standard.category == category).order_by(Standard.name).all()

    @staticmethod
    def get_for_job_title(db: Session, job_title_id: UUID) -> List[Standard]:
        """Get standards applicable to a job title."""
        return db.query(Standard).filter(Standard.applicable_to.contains([job_title_id])).all()

    @staticmethod
    def update(db: Session, standard_id: UUID, schema: StandardUpdate) -> Optional[Standard]:
        """Update standard."""
        standard = db.query(Standard).filter(Standard.id == standard_id).first()
        if not standard:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(standard, field, value)

        db.commit()
        db.refresh(standard)

        return standard

    @staticmethod
    def delete(db: Session, standard_id: UUID) -> bool:
        """Delete standard."""
        standard = db.query(Standard).filter(Standard.id == standard_id).first()
        if not standard:
            return False

        db.delete(standard)
        db.commit()

        return True
