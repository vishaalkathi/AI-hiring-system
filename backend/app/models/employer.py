from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl

class EmployerProfileCreate(BaseModel):
    company_name: str
    company_description: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    company_location: Optional[str] = None

class EmployerProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    company_location: Optional[str] = None


class EmployerProfileResponse(BaseModel):
    user_id: UUID

    company_name: str
    company_description: Optional[str] = None
    website_url: Optional[str] = None
    company_location: Optional[str] = None