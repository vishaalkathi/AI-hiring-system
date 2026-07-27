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

def build_candidate_features(user_id: str) -> CombinedFeatures:

    candidate = get_candidate_profile(user_id) or {}

    github = get_github_profile(user_id) or {}

    leetcode = get_leetcode_profile(user_id) or {}

    return CombinedFeatures(

        # Candidate
        current_location=candidate.get("current_location"),

        # GitHub
        repo_count=github.get("public_repos", 0),
        github_followers=github.get("followers", 0),
        github_stars=github.get("total_stars", 0),
        github_languages=github.get("languages", []),

        # LeetCode
        total_solved=leetcode.get("total_solved", 0),

        easy_solved=leetcode.get("easy_solved", 0),
        medium_solved=leetcode.get("medium_solved", 0),
        hard_solved=leetcode.get("hard_solved", 0),

        streak=leetcode.get("streak", 0),
        active_days=leetcode.get("active_days", 0),

        language_diversity=leetcode.get("language_diversity", 0),
        language_list=leetcode.get("language_list", []),

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
    )