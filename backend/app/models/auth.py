from backend.app.models.enums import UserRole

from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserRegister(BaseModel):
    name: str = Field(min_length = 2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length = 128)
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    name: str
    email: EmailStr
    role: UserRole