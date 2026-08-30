from datetime import datetime
from typing import List, Optional
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

    parsed_role: Optional[str] = None
    parsed_skills: Optional[List[str]] = None
    parsed_experience: Optional[float] = None

    resume_parsed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CandidateProfileDB(CandidateProfileResponse):
    resume_text: Optional[str]