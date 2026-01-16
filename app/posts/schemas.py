from pydantic import BaseModel, Field
from datetime import datetime


class PostCreate(BaseModel):
    """Schema for creating a post."""
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class PostRead(BaseModel):
    """Schema for reading a post."""
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    """Schema for updating a post."""
    title: str | None = Field(None, min_length=1, max_length=255)
    content: str | None = Field(None, min_length=1)
    
    class Config:
        extra = "forbid"
