from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime


class UserCreate(BaseModel):
    """
    Schema for user registration.
    
    Accepts plain password (will be hashed before storage).
    """
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Ensure password meets security requirements."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class UserRead(BaseModel):
    """
    Schema for user responses.
    
    IMPORTANT: Never includes sensitive data like passwords!
    """
    id: int
    email: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """
    Schema for updating user.
    
    All fields are optional (only update what's provided).
    """
    email: EmailStr | None = None
    is_active: bool | None = None
    
    class Config:
        extra = "forbid"  # Reject unknown fields


class UserLogin(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str
