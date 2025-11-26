"""Standard schemas."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class StandardBase(BaseModel):
    """Base schema for Standard."""

    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., min_length=1, max_length=50)
    category: str = Field(..., min_length=1, max_length=100)
    path: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    applicable_to: List[UUID] = Field(default_factory=list)  # Job title IDs
    related_tools: List[UUID] = Field(default_factory=list)  # Technology IDs
    difficulty: int = Field(default=3, ge=1, le=5)
    importance_by_grade: Dict[str, int] = Field(default_factory=dict)


class StandardCreate(StandardBase):
    """Schema for creating Standard."""
    pass


class StandardUpdate(BaseModel):
    """Schema for updating Standard."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    path: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    applicable_to: Optional[List[UUID]] = None
    related_tools: Optional[List[UUID]] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    importance_by_grade: Optional[Dict[str, int]] = None


class StandardResponse(StandardBase):
    """Schema for Standard response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
