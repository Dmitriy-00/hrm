"""Industry schemas."""

from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class IndustryBase(BaseModel):
    """Base schema for Industry."""

    name: str = Field(..., min_length=1, max_length=255)
    path: str = Field(..., min_length=1, max_length=500)
    parent_id: Optional[UUID] = None
    description: Optional[str] = None
    common_tech_stack: List[UUID] = Field(default_factory=list)
    compliance_requirements: List[str] = Field(default_factory=list)
    typical_challenges: List[str] = Field(default_factory=list)


class IndustryCreate(IndustryBase):
    """Schema for creating Industry."""
    pass


class IndustryUpdate(BaseModel):
    """Schema for updating Industry."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    path: Optional[str] = Field(None, min_length=1, max_length=500)
    parent_id: Optional[UUID] = None
    description: Optional[str] = None
    common_tech_stack: Optional[List[UUID]] = None
    compliance_requirements: Optional[List[str]] = None
    typical_challenges: Optional[List[str]] = None


class IndustryResponse(IndustryBase):
    """Schema for Industry response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndustryTree(IndustryResponse):
    """Schema for Industry with children."""

    children: List['IndustryTree'] = Field(default_factory=list)

    class Config:
        from_attributes = True
