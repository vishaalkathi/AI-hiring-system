from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel



class ApplicationUpdate(BaseModel):
    application_status: str

class ApplicationResponse(BaseModel):
    application_id: UUID
    candidate_user_id: UUID
    job_id: UUID
    
    application_status: str

    match_score: Optional[Decimal] = None

    created_at: datetime
    updated_at: datetime

