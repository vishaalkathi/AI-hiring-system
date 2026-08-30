from typing import Dict

from backend.app.services.ml_matcher import (
    predict_match,
    calculate_text_similarity,
)
from backend.app.services.job_feature_builder import (
    parse_required_experience,
)


class MatchingEngine:
    """
    ML-based candidate-job matching engine.

    Builds the same feature set used during model training
    and passes it to the trained XGBoost regression model.
    """

    def calculate_match_score(
        self,
        candidate: Dict,
        job: Dict,
    ) -> Dict:

        features = self._build_features(
            candidate,
            job,
        )

        prediction = predict_match(
            features
        )

        return {
            "match_score": prediction[
                "relevance_score"
            ],
            "fit_level": prediction[
                "fit_level"
            ],
            "breakdown": self._build_breakdown(
                features
            ),
        }

    # ========================================================
    # FEATURE BUILDING
    # ========================================================

    def _build_features(
        self,
        candidate: Dict,
        job: Dict,
    ) -> Dict:

        # ----------------------------------------------------
        # SKILLS
        # ----------------------------------------------------

        required_skills = self._extract_job_skills(
            job
        )

        candidate_skills = self._extract_candidate_skills(
            candidate
        )

        overlap = (
            required_skills
            & candidate_skills
        )

        union = (
            required_skills
            | candidate_skills
        )

        overlap_count = len(overlap)

        # Fraction of job skills candidate has
        if required_skills:
            job_skill_coverage = (
                overlap_count
                / len(required_skills)
            )
        else:
            job_skill_coverage = 0.0

        # Fraction of candidate skills relevant to job
        if candidate_skills:
            candidate_skill_coverage = (
                overlap_count
                / len(candidate_skills)
            )
        else:
            candidate_skill_coverage = 0.0

        # Jaccard
        if union:
            skill_jaccard = (
                overlap_count
                / len(union)
            )
        else:
            skill_jaccard = 0.0

        # ----------------------------------------------------
        # ROLE SIMILARITY
        # ----------------------------------------------------

        candidate_role = str(
            candidate.get(
                "candidate_role",
                ""
            )
        ).lower().strip()

        job_title = str(
            job.get(
                "title",
                ""
            )
        ).lower().strip()

        candidate_tokens = set(
            candidate_role.split()
        )

        job_tokens = set(
            job_title.split()
        )

        role_union = (
            candidate_tokens
            | job_tokens
        )

        if role_union:
            role_similarity = (
                len(
                    candidate_tokens
                    & job_tokens
                )
                / len(role_union)
            )
        else:
            role_similarity = 0.0

        # ----------------------------------------------------
        # TEXT SIMILARITY
        # ----------------------------------------------------

        resume = candidate.get(
            "candidate_resume",
            candidate.get(
                "resume",
                ""
            )
        )

        job_description = job.get(
            "description",
            ""
        )

        text_similarity = calculate_text_similarity(
            resume,
            job_description,
        )

        # ----------------------------------------------------
        # EXPERIENCE
        # ----------------------------------------------------

        candidate_experience = float(
            candidate.get(
                "candidate_experience",
                0
            )
        )

        required_experience = parse_required_experience(
            job.get("experience_required")
        )

        experience_gap = (
            candidate_experience
            - required_experience
        )

        # ----------------------------------------------------
        # GITHUB
        # ----------------------------------------------------

        github_public_repos = candidate.get(
            "github_public_repos",
            candidate.get(
                "repo_count",
                0
            )
        )

        github_followers = candidate.get(
            "github_followers",
            0
        )

        github_total_stars = candidate.get(
            "github_total_stars",
            candidate.get(
                "github_stars",
                0
            )
        )

        github_languages = candidate.get(
            "github_languages",
            []
        )

        github_language_diversity = candidate.get(
            "github_language_diversity",
            len(github_languages)
        )

        github_active_repos = candidate.get(
            "github_active_repos",
            0
        )

        # ----------------------------------------------------
        # LEETCODE
        # ----------------------------------------------------

        leetcode_total_solved = candidate.get(
            "total_solved",
            0
        )

        leetcode_easy = candidate.get(
            "easy_solved",
            0
        )

        leetcode_medium = candidate.get(
            "medium_solved",
            0
        )

        leetcode_hard = candidate.get(
            "hard_solved",
            0
        )

        leetcode_contest_rating = candidate.get(
            "contest_rating",
            0
        )

        leetcode_contest_percentile = candidate.get(
            "contest_rank_percentile",
            100
        )

        leetcode_contests_attended = candidate.get(
            "contest_attended",
            0
        )

        leetcode_streak = candidate.get(
            "streak",
            0
        )

        leetcode_active_days = candidate.get(
            "active_days",
            0
        )

        # ----------------------------------------------------
        # DSA STRENGTHS
        # ----------------------------------------------------

        dp_strength = candidate.get(
            "dp_strength",
            0
        )

        graph_strength = candidate.get(
            "graph_strength",
            0
        )

        greedy_strength = candidate.get(
            "greedy_strength",
            0
        )

        tree_strength = candidate.get(
            "tree_strength",
            0
        )

        binary_search_strength = candidate.get(
            "binary_search_strength",
            0
        )

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        return {

            "job_skill_coverage":
                job_skill_coverage,

            "skill_jaccard":
                skill_jaccard,

            "role_similarity":
                role_similarity,

            "text_similarity":
                text_similarity,

            "skill_overlap_count":
                overlap_count,

            "skill_overlap_ratio":
                job_skill_coverage,

            "candidate_skill_coverage":
                candidate_skill_coverage,

            "candidate_experience":
                candidate_experience,

            "experience_gap":
                experience_gap,

            "github_public_repos":
                github_public_repos,

            "github_followers":
                github_followers,

            "github_total_stars":
                github_total_stars,

            "github_language_diversity":
                github_language_diversity,

            "github_active_repos":
                github_active_repos,

            "leetcode_total_solved":
                leetcode_total_solved,

            "leetcode_easy":
                leetcode_easy,

            "leetcode_medium":
                leetcode_medium,

            "leetcode_hard":
                leetcode_hard,

            "leetcode_contest_rating":
                leetcode_contest_rating,

            "leetcode_contest_percentile":
                leetcode_contest_percentile,

            "leetcode_contests_attended":
                leetcode_contests_attended,

            "leetcode_streak":
                leetcode_streak,

            "leetcode_active_days":
                leetcode_active_days,

            "dp_strength":
                dp_strength,

            "graph_strength":
                graph_strength,

            "greedy_strength":
                greedy_strength,

            "tree_strength":
                tree_strength,

            "binary_search_strength":
                binary_search_strength,
        }

    # ========================================================
    # SKILL HELPERS
    # ========================================================

    def _extract_job_skills(
        self,
        job: Dict,
    ) -> set:

        required_skills = job.get(
            "required_skills",
            {}
        )

        if isinstance(
            required_skills,
            dict
        ):
            return {
                str(skill)
                .lower()
                .strip()
                for skill in required_skills.keys()
            }

        if isinstance(
            required_skills,
            list
        ):
            return {
                str(skill)
                .lower()
                .strip()
                for skill in required_skills
            }

        return set()


    def _extract_candidate_skills(
        self,
        candidate: Dict,
    ) -> set:

        candidate_skills = candidate.get(
            "candidate_skills",
            []
        )

        if isinstance(candidate_skills, list):
            return {
                str(skill)
                .lower()
                .strip()
                for skill in candidate_skills
                if str(skill).strip()
            }

        return set()


    # ========================================================
    # BREAKDOWN
    # ========================================================

    def _build_breakdown(
        self,
        features: Dict,
    ) -> Dict:

        return {

            "skill_coverage": round(
                features[
                    "job_skill_coverage"
                ] * 100,
                2
            ),

            "role_similarity": round(
                features[
                    "role_similarity"
                ] * 100,
                2
            ),

            "text_similarity": round(
                features[
                    "text_similarity"
                ] * 100,
                2
            ),

            "github": {

                "repositories":
                    features[
                        "github_public_repos"
                    ],

                "stars":
                    features[
                        "github_total_stars"
                    ],

                "followers":
                    features[
                        "github_followers"
                    ],
            },

            "leetcode": {

                "total_solved":
                    features[
                        "leetcode_total_solved"
                    ],

                "easy":
                    features[
                        "leetcode_easy"
                    ],

                "medium":
                    features[
                        "leetcode_medium"
                    ],

                "hard":
                    features[
                        "leetcode_hard"
                    ],

                "contest_rating":
                    features[
                        "leetcode_contest_rating"
                    ],
            },
        }