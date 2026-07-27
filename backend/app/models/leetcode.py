from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class LeetCodeProfileCreate(BaseModel):
    leetcode_username: str


class LeetCodeProfileResponse(BaseModel):
    user_id: UUID

    leetcode_username: str

    language_diversity: int
    language_list: List[str]

    primary_language: Optional[str]
    primary_language_share: float

    skill_stats: Dict[str, int]

    contest_rating: float
    contest_rank_percentile: float
    contest_attended: int

    total_solved: int
    easy_solved: int
    medium_solved: int
    hard_solved: int

    streak: int
    active_days: int

    last_synced_at: Optional[datetime]