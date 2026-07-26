from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class GitHubProfileCreate(BaseModel):
    github_username: str

class GitHubProfileResponse(BaseModel):
    user_id: UUID
    github_username: str

    public_repos: int
    followers: int
    total_stars: int

    languages: List[str]

    active_repos: int

    last_synced_at: Optional[datetime]

