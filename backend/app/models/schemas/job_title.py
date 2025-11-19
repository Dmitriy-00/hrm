"""Job Title schemas."""

from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class JobTitleBase(BaseModel):
    """Base schema for Job Title."""

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    parent_id: Optional[UUID] = None
    aliases: List[str] = Field(default_factory=list)
    description: Optional[str] = None

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Validate slug format."""
        if not v.replace('-', '').replace('_', '').replace('.', '').isalnum():
            raise ValueError('Slug must contain only alphanumeric characters, hyphens, underscores, and dots')
        return v.lower()


class JobTitleCreate(JobTitleBase):
    """Schema for creating Job Title."""
    pass


class JobTitleUpdate(BaseModel):
    """Schema for updating Job Title."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    parent_id: Optional[UUID] = None
    aliases: Optional[List[str]] = None
    description: Optional[str] = None


class JobTitleResponse(JobTitleBase):
    """Schema for Job Title response."""

    id: UUID
    level: int
    path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobTitleTree(JobTitleResponse):
    """Schema for Job Title with children."""

    children: List['JobTitleTree'] = Field(default_factory=list)

    class Config:
        from_attributes = True
