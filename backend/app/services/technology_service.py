"""Technology service."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models.technology import Technology
from app.models.schemas.technology import TechnologyCreate, TechnologyUpdate
from app.utils.hierarchy import build_path


class TechnologyService:
    """Service for Technology operations."""

    @staticmethod
    def create(db: Session, schema: TechnologyCreate) -> Technology:
        """Create new technology."""
        # Get parent if exists
        parent_path = None
        if schema.parent_id:
            parent = db.query(Technology).filter(Technology.id == schema.parent_id).first()
            if not parent:
                raise ValueError(f"Parent technology with id {schema.parent_id} not found")
            parent_path = parent.path

        # Build path
        path = build_path(schema.slug, parent_path)

        # Create technology
        technology = Technology(
            name=schema.name,
            slug=schema.slug,
            category=schema.category,
            parent_id=schema.parent_id,
            path=path,
            tags=schema.tags,
            related_technologies=schema.related_technologies,
            difficulty_level=schema.difficulty_level,
            popularity_score=schema.popularity_score,
            metadata=schema.metadata,
        )

        db.add(technology)
        db.commit()
        db.refresh(technology)

        return technology

    @staticmethod
    def get(db: Session, technology_id: UUID) -> Optional[Technology]:
        """Get technology by ID."""
        return db.query(Technology).filter(Technology.id == technology_id).first()

    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Technology]:
        """Get technology by slug."""
        return db.query(Technology).filter(Technology.slug == slug).first()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Technology]:
        """Get all technologies with optional filters."""
        query = db.query(Technology)

        if category:
            query = query.filter(Technology.category == category)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Technology.name.ilike(search_pattern),
                    Technology.slug.ilike(search_pattern),
                )
            )

        return query.order_by(Technology.popularity_score.desc(), Technology.name).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_category(db: Session, category: str) -> List[Technology]:
        """Get technologies by category."""
        return db.query(Technology).filter(Technology.category == category).order_by(Technology.name).all()

    @staticmethod
    def get_popular(db: Session, limit: int = 10) -> List[Technology]:
        """Get most popular technologies."""
        return db.query(Technology).order_by(Technology.popularity_score.desc()).limit(limit).all()

    @staticmethod
    def get_by_tags(db: Session, tags: List[str]) -> List[Technology]:
        """Get technologies by tags."""
        query = db.query(Technology)
        for tag in tags:
            query = query.filter(Technology.tags.contains([tag]))
        return query.all()

    @staticmethod
    def get_related(db: Session, technology_id: UUID) -> List[Technology]:
        """Get related technologies."""
        technology = db.query(Technology).filter(Technology.id == technology_id).first()
        if not technology or not technology.related_technologies:
            return []

        return db.query(Technology).filter(Technology.id.in_(technology.related_technologies)).all()

    @staticmethod
    def update(db: Session, technology_id: UUID, schema: TechnologyUpdate) -> Optional[Technology]:
        """Update technology."""
        technology = db.query(Technology).filter(Technology.id == technology_id).first()
        if not technology:
            return None

        # Update fields
        update_data = schema.model_dump(exclude_unset=True)

        # If parent_id or slug changed, recalculate path
        if "parent_id" in update_data or "slug" in update_data:
            parent_path = None
            if update_data.get("parent_id"):
                parent = db.query(Technology).filter(Technology.id == update_data["parent_id"]).first()
                if not parent:
                    raise ValueError(f"Parent technology not found")
                parent_path = parent.path

            slug = update_data.get("slug", technology.slug)
            path = build_path(slug, parent_path)
            update_data["path"] = path

        for field, value in update_data.items():
            setattr(technology, field, value)

        db.commit()
        db.refresh(technology)

        return technology

    @staticmethod
    def delete(db: Session, technology_id: UUID) -> bool:
        """Delete technology."""
        technology = db.query(Technology).filter(Technology.id == technology_id).first()
        if not technology:
            return False

        db.delete(technology)
        db.commit()

        return True

    @staticmethod
    def update_popularity(db: Session, technology_id: UUID, score: int) -> Optional[Technology]:
        """Update technology popularity score."""
        technology = db.query(Technology).filter(Technology.id == technology_id).first()
        if not technology:
            return None

        technology.popularity_score = max(0, min(100, score))
        db.commit()
        db.refresh(technology)

        return technology
