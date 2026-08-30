from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class GitHubFeatures(BaseModel):
    public_repos: int = 0
    followers: int = 0
    total_stars: int = 0
    languages: List[str] = Field(default_factory=list)
    active_repos: int = 0

    # Important: distinguish "no profile" from "empty profile"
    available: bool = False


class LeetCodeFeatures(BaseModel):
    language_diversity: int = 0
    language_list: List[str] = Field(default_factory=list)

    primary_language: Optional[str] = None
    primary_language_share: float = 0.0

    skill_stats: Dict[str, int] = Field(default_factory=dict)

    contest_rating: float = 0.0
    contest_rank_percentile: float = 100.0
    contest_attended: int = 0

    total_solved: int = 0
    easy: int = 0
    medium: int = 0
    hard: int = 0

    streak: int = 0
    active_days: int = 0

    available: bool = False


class CombinedFeatures(BaseModel):

    # Candidate profile
    current_location: Optional[str] = None

    # Resume
    resume: str = ""
    candidate_role: str = ""
    candidate_skills: List[str] = Field(default_factory=list)
    candidate_experience: float = 0.0

    # Evidence availability
    github_available: bool = False
    leetcode_available: bool = False

    # GitHub
    repo_count: int = 0
    github_followers: int = 0
    github_stars: int = 0
    github_languages: List[str] = Field(default_factory=list)
    active_repos: int = 0

    # LeetCode
    total_solved: int = 0
    easy_solved: int = 0
    medium_solved: int = 0
    hard_solved: int = 0

    streak: int = 0
    active_days: int = 0

    language_diversity: int = 0
    language_list: List[str] = Field(default_factory=list)

    primary_language: Optional[str] = None
    primary_language_share: float = 0.0

    contest_rating: float = 0.0
    contest_rank_percentile: float = 100.0
    contest_attended: int = 0

    skill_stats: Dict[str, int] = Field(default_factory=dict)

    # DSA strengths
    dp_strength: float = 0.0
    graph_strength: float = 0.0
    greedy_strength: float = 0.0
    tree_strength: float = 0.0
    binary_search_strength: float = 0.0

class Candidate(BaseModel):
    username: str

    github: GitHubFeatures
    leetcode: LeetCodeFeatures

    combined_features: CombinedFeatures


class JobFeatures(BaseModel):
    job_id: Optional[str] = None

    title: str
    description: str

    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_required: float = 0.0

    required_skills: List[str] = Field(
        default_factory=list
    )

    preferred_skills: List[str] = Field(
        default_factory=list
    )

    status: str = "OPEN"