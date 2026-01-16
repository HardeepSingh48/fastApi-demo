from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class User(SQLModel, table=True):
    """
    User database model.
    
    IMPORTANT: Never expose this model directly in API responses!
    Use UserRead schema instead to exclude hashed_password.
    """
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)  # ✅ Store hashed passwords only
    role: str = Field(default="user", max_length=50)  # "user" or "admin"
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    posts: list["Post"] = Relationship(back_populates="author")


class Post(SQLModel, table=True):
    """Post database model."""
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    content: str
    author_id: int = Field(foreign_key="user.id")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    author: User = Relationship(back_populates="posts")