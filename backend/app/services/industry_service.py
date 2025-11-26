"""Industry service."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models.industry import Industry
from app.models.schemas.industry import IndustryCreate, IndustryUpdate


class IndustryService:
    """Service for Industry operations."""

    @staticmethod
    def create(db: Session, schema: IndustryCreate) -> Industry:
        """Create new industry."""
        industry = Industry(
            name=schema.name,
            path=schema.path,
            parent_id=schema.parent_id,
            description=schema.description,
            common_tech_stack=schema.common_tech_stack,
            compliance_requirements=schema.compliance_requirements,
            typical_challenges=schema.typical_challenges,
        )

        db.add(industry)
        db.commit()
        db.refresh(industry)

        return industry

    @staticmethod
    def get(db: Session, industry_id: UUID) -> Optional[Industry]:
        """Get industry by ID."""
        return db.query(Industry).filter(Industry.id == industry_id).first()

    @staticmethod
    def get_by_path(db: Session, path: str) -> Optional[Industry]:
        """Get industry by path."""
        return db.query(Industry).filter(Industry.path == path).first()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
    ) -> List[Industry]:
        """Get all industries with optional search."""
        query = db.query(Industry)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Industry.name.ilike(search_pattern),
                    Industry.path.ilike(search_pattern),
                )
            )

        return query.order_by(Industry.path).offset(skip).limit(limit).all()

    @staticmethod
    def get_roots(db: Session) -> List[Industry]:
        """Get root industries (no parent)."""
        return db.query(Industry).filter(Industry.parent_id.is_(None)).order_by(Industry.name).all()

    @staticmethod
    def get_children(db: Session, parent_id: UUID) -> List[Industry]:
        """Get direct children of an industry."""
        return db.query(Industry).filter(Industry.parent_id == parent_id).order_by(Industry.name).all()

    @staticmethod
    def update(db: Session, industry_id: UUID, schema: IndustryUpdate) -> Optional[Industry]:
        """Update industry."""
        industry = db.query(Industry).filter(Industry.id == industry_id).first()
        if not industry:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(industry, field, value)

        db.commit()
        db.refresh(industry)

        return industry

    @staticmethod
    def delete(db: Session, industry_id: UUID) -> bool:
        """Delete industry."""
        industry = db.query(Industry).filter(Industry.id == industry_id).first()
        if not industry:
            return False

        # Check if has children
        children_count = db.query(Industry).filter(Industry.parent_id == industry_id).count()
        if children_count > 0:
            raise ValueError("Cannot delete industry with children")

        db.delete(industry)
        db.commit()

        return True
