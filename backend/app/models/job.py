from uuid import UUID
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str

    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_required: Optional[str] = None

    required_skills: List[str] = []
    preferred_skills: List[str] = []


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_required: Optional[str] = None

    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None

    status: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_required: Optional[str] = None

    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None

    status: Optional[str] = None

class JobResponse(BaseModel):
    job_id: UUID
    employer_user_id: UUID

    title: str
    description: str

    location: Optional[str]
    employment_type: Optional[str]
    experience_required: Optional[str]

    required_skills: List[str]
    preferred_skills: List[str]

    status: str

    created_at: datetime
    updated_at: datetime

