import json

from backend.app.models.features import CombinedFeatures

from backend.app.db.repositories.candidate_repository import (
    get_candidate_profile,
)

from backend.app.db.repositories.github_repository import (
    get_github_profile,
)

from backend.app.db.repositories.leetcode_repository import (
    get_leetcode_profile
)

def _normalize_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        try:
            parsed = json.loads(value)

            if isinstance(parsed, list):
                return parsed

        except json.JSONDecodeError:
            pass

    return []

def build_candidate_features(user_id: str) -> CombinedFeatures:

    candidate = get_candidate_profile(user_id) or {}

    github = get_github_profile(user_id) or {}

    leetcode = get_leetcode_profile(user_id) or {}

    skill_stats = leetcode.get("skill_stats", {}) or {}
    return CombinedFeatures(

        # Candidate
        current_location=candidate.get("current_location"),

        #Resume
        resume=candidate.get("resume_text") or "",
        candidate_role=candidate.get("parsed_role") or "",
        candidate_skills= _normalize_list(
            candidate.get("parsed_skills")
        ),
        candidate_experience=float(
            candidate.get("parsed_experience") or 0
        ),

        # Evidence availability
        github_available=bool(github),
        leetcode_available=bool(leetcode),

        # GitHub
        repo_count=github.get("public_repos", 0),
        github_followers=github.get("followers", 0),
        github_stars=github.get("total_stars", 0),
        github_languages=_normalize_list(
            github.get("languages")
        ),
        active_repos=github.get(
            "active_repos", 0
        ),

        # LeetCode
        total_solved=leetcode.get("total_solved", 0),

        easy_solved=leetcode.get("easy_solved", 0),
        medium_solved=leetcode.get("medium_solved", 0),
        hard_solved=leetcode.get("hard_solved", 0),

        streak=leetcode.get("streak", 0),
        active_days=leetcode.get("active_days", 0),

        language_diversity=leetcode.get("language_diversity", 0),
        language_list=_normalize_list(
            leetcode.get("language_list")
        ),

        primary_language=leetcode.get("primary_language"),
        primary_language_share=leetcode.get(
            "primary_language_share",
            0.0,
        ),

        contest_rating=leetcode.get("contest_rating", 0),
        contest_rank_percentile=leetcode.get(
            "contest_rank_percentile",
            100,
        ),
        contest_attended=leetcode.get("contest_attended", 0),

        skill_stats=leetcode.get("skill_stats", {}),

        dp_strength = skill_stats.get("dynamic_programming", 0),
        graph_strength = skill_stats.get("graph_theory", 0),
        greedy_strength = skill_stats.get("greedy", 0),
        tree_strength = skill_stats.get("tree", 0),
        binary_search_strength = skill_stats.get("binary_search", 0),
    )