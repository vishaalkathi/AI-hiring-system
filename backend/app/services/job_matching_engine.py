from backend.app.models.features import (
    CombinedFeatures,
    JobFeatures,
)


class MatchingEngine:
    """
    Rule-based candidate-job matching engine.

    The engine only compares already-built feature vectors.
    It does not access the database or external APIs.
    """

    def calculate_match_score(
        self,
        candidate: CombinedFeatures,
        job: JobFeatures,
    ) -> dict:

        dsa_score = self._calculate_dsa_score(
            candidate
        )

        skills_score = self._calculate_skills_score(
            candidate,
            job,
        )

        github_score = self._calculate_github_score(
            candidate
        )

        # Fixed initial weights
        final_score = (
            dsa_score * 0.40
            + skills_score * 0.40
            + github_score * 0.20
        )

        return {
            "match_score": round(final_score, 2),
            "fit": self._get_fit(final_score),
            "breakdown": {
                "dsa": round(dsa_score, 2),
                "skills": round(skills_score, 2),
                "github": round(github_score, 2),
            },
        }

    def _calculate_dsa_score(
        self,
        candidate: CombinedFeatures,
    ) -> float:

        solved = candidate.total_solved

        if solved >= 500:
            return 100.0

        elif solved >= 300:
            return 80.0

        elif solved >= 200:
            return 60.0

        elif solved >= 100:
            return 40.0

        return 20.0

    def _calculate_skills_score(
        self,
        candidate: CombinedFeatures,
        job: JobFeatures,
    ) -> float:

        required_skills = job.required_skills

        if not required_skills:
            return 100.0

        candidate_skills = {
            skill.lower()
            for skill in candidate.skill_stats.keys()
        }

        matched = sum(
            1
            for skill in required_skills
            if skill.lower() in candidate_skills
        )

        return (
            matched / len(required_skills)
        ) * 100

    def _calculate_github_score(
        self,
        candidate: CombinedFeatures,
    ) -> float:

        repo_count = candidate.repo_count
        stars = candidate.github_stars

        score = (
            repo_count * 2
            + stars * 0.5
        )

        return min(score, 100.0)

    @staticmethod
    def _get_fit(score: float) -> str:

        if score >= 80:
            return "Strong Match"

        elif score >= 60:
            return "Good Match"

        elif score >= 40:
            return "Average Match"

        return "Weak Match"