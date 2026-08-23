from typing import Dict

from backend.app.models.features import (
    CombinedFeatures,
    JobFeatures,
)


def _normalize(value: str) -> str:
    return value.strip().lower()


def _match_ratio(
    candidate_values: list[str],
    required_values: list[str],
) -> float:

    if not required_values:
        return 0.0

    candidate_set = {
        _normalize(value)
        for value in candidate_values
    }

    required_set = {
        _normalize(value)
        for value in required_values
    }

    matched = candidate_set.intersection(required_set)

    return len(matched) / len(required_set)


def build_matching_features(
    candidate: CombinedFeatures,
    job: JobFeatures,
) -> Dict[str, float]:

    # -----------------------------------------
    # Candidate evidence
    # -----------------------------------------

    features = {

        "github_available": int(
            candidate.github_available
        ),

        "leetcode_available": int(
            candidate.leetcode_available
        ),

        # -------------------------------------
        # GitHub
        # -------------------------------------

        "repo_count": candidate.repo_count,

        "github_followers": candidate.github_followers,

        "github_stars": candidate.github_stars,

        "active_repos": candidate.active_repos,

        # -------------------------------------
        # LeetCode
        # -------------------------------------

        "total_solved": candidate.total_solved,

        "easy_solved": candidate.easy_solved,

        "medium_solved": candidate.medium_solved,

        "hard_solved": candidate.hard_solved,

        "streak": candidate.streak,

        "active_days": candidate.active_days,

        "language_diversity": candidate.language_diversity,

        "primary_language_share":
            candidate.primary_language_share,

        "contest_rating":
            candidate.contest_rating,

        "contest_rank_percentile":
            candidate.contest_rank_percentile,

        "contest_attended":
            candidate.contest_attended,
    }

    # -----------------------------------------
    # Skill matching
    # -----------------------------------------

    candidate_skills = list(
        candidate.skill_stats.keys()
    )

    features["required_skill_match_ratio"] = (
        _match_ratio(
            candidate_skills,
            job.required_skills,
        )
    )

    features["preferred_skill_match_ratio"] = (
        _match_ratio(
            candidate_skills,
            job.preferred_skills,
        )
    )

    return features