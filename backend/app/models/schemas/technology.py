"""Technology schemas."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class TechnologyBase(BaseModel):
    """Base schema for Technology."""

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=50)
    parent_id: Optional[UUID] = None
    tags: List[str] = Field(default_factory=list)
    related_technologies: List[UUID] = Field(default_factory=list)
    difficulty_level: int = Field(default=3, ge=1, le=5)
    popularity_score: int = Field(default=50, ge=0, le=100)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Validate slug format."""
        if not v.replace('-', '').replace('_', '').replace('.', '').isalnum():
            raise ValueError('Slug must contain only alphanumeric characters, hyphens, underscores, and dots')
        return v.lower()


class TechnologyCreate(TechnologyBase):
    """Schema for creating Technology."""
    pass


class TechnologyUpdate(BaseModel):
    """Schema for updating Technology."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    parent_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    related_technologies: Optional[List[UUID]] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    popularity_score: Optional[int] = Field(None, ge=0, le=100)
    metadata: Optional[Dict[str, Any]] = None


class TechnologyResponse(TechnologyBase):
    """Schema for Technology response."""

    id: UUID
    path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TechnologyTree(TechnologyResponse):
    """Schema for Technology with children."""

    children: List['TechnologyTree'] = Field(default_factory=list)

    class Config:
        from_attributes = True
