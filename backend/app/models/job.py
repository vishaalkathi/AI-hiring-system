from pydantic import BaseModel
from typing import List, Dict

class Job(BaseModel):
    title: str
    description: str
    required_skills: List[str]

    min_dsa_score: int = 0
    min_github_score: int = 0

    weights: Dict[str,float] = {
        "dsa": 0.4,
        "skills": 0.4,
        "github": 0.2
    }