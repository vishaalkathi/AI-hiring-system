from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl

class CandidateProfileCreate(BaseModel):
    phone: Optional[str] = None
    current_location: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None

class CandidateProfileUpdate(BaseModel):
    phone: Optional[str] = None
    current_location: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None

class CandidateProfileResponse(BaseModel):
    user_id: UUID
    phone: Optional[str]
    current_location: Optional[str]

    linkedin_url: Optional[HttpUrl]
    portfolio_url: Optional[HttpUrl]

    resume_url: Optional[str]
    predicted_score: Optional[float]

    model_config = ConfigDict(from_attributes=True)

class CandidateProfileDB(CandidateProfileResponse):
    resume_text: Optional[str]