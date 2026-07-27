from pydantic import BaseModel,Field
from typing import Dict, List, Optional


class GitHubFeatures(BaseModel):
    public_repos: int = 0
    followers: int = 0
    total_stars: int = 0
    languages: List[str] = []
    active_repos: int = 0


class LeetCodeFeatures(BaseModel):
    language_diversity: int = 0
    language_list: List[str] = []

    primary_language: Optional[str] = None
    primary_language_share: float = 0.0

    skill_stats: Dict[str, int] = {}

    contest_rating: float = 0.0
    contest_rank_percentile: float = 100.0
    contest_attended: int = 0

    total_solved: int = 0
    easy: int = 0
    medium: int = 0
    hard: int = 0

    streak: int = 0
    active_days: int = 0

# -------------------------
# Combined ML Feature Vector
# -------------------------
class CombinedFeatures(BaseModel):

    # -------------------------
    # Candidate Profile
    # -------------------------

    current_location: Optional[str] = None

    # -------------------------
    # GitHub Features
    # -------------------------

    repo_count: int = 0
    github_followers: int = 0
    github_stars: int = 0

    github_languages: List[str] = []

    active_repos: int = 0

    # -------------------------
    # LeetCode Features
    # -------------------------

    total_solved: int = 0

    easy_solved: int = 0
    medium_solved: int = 0
    hard_solved: int = 0

    streak: int = 0
    active_days: int = 0

    language_diversity: int = 0
    language_list: List[str] = []

    primary_language: Optional[str] = None
    primary_language_share: float = 0.0

    contest_rating: float = 0.0
    contest_rank_percentile: float = 100.0
    contest_attended: int = 0

    skill_stats: Dict[str, int] = {}


# -------------------------
# FINAL CANDIDATE OBJECT (DELETE THIS LATER)
# -------------------------
class Candidate(BaseModel):
    username: str

    github: GitHubFeatures
    leetcode: LeetCodeFeatures

    combined_features: CombinedFeatures

class JobFeatures(BaseModel):
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