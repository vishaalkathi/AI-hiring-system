from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class ApplicationUpdate(BaseModel):
    application_status: str


class ApplicationResponse(BaseModel):

    application_id: UUID

    candidate_user_id: UUID

    job_id: UUID

    application_status: str

    match_score: Optional[Decimal] = None

    # ========================================================
    # RESUME SNAPSHOT
    # ========================================================

    resume_snapshot: Optional[str] = None

    parsed_role_snapshot: Optional[str] = None

    parsed_skills_snapshot: List[str] = Field(
        default_factory=list
    )

    parsed_experience_snapshot: Optional[float] = None

    created_at: datetime

    updated_at: datetime
