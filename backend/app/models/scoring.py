from pydantic import BaseModel
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
# Combined ML Feature Vector (IMPORTANT PART)
# -------------------------
class CombinedFeatures(BaseModel):
    total_solved: int = 0
    streak: int = 0
    active_days: int = 0

    repo_count: int = 0
    github_stars: int = 0

    language_diversity: int = 0

    # IMPORTANT: keep as dict for ML feature expansion
    skill_stats: Dict[str, int] = {}


# -------------------------
# FINAL CANDIDATE OBJECT
# -------------------------
class Candidate(BaseModel):
    username: str

    github: GitHubFeatures
    leetcode: LeetCodeFeatures

    combined_features: CombinedFeatures