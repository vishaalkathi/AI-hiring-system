from pydantic import BaseModel,Field
from typing import List, Dict,Optional

class Job(BaseModel):
    job_id: Optional[str] = None
    title: str
    description: str

    job_type: str = "SDE"
    experience_level: str = "entry"

    required_skills: Dict[str, int]

    preferred_languages: List[str] = []

    min_dsa_score: int = 0
    min_github_score: int = 0

    weights: Dict[str, float] = Field(default_factory=lambda: {
        "dsa": 0.4,
        "skills": 0.4,
        "github": 0.2
    })