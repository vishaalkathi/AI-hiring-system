from typing import Dict


class MatchingEngine:
    """
    Rule-based matching engine.

    Later this class can be replaced with an ML model
    without changing the rest of the backend.
    """

    def calculate_match_score(
        self,
        candidate: Dict,
        job: Dict,
    ) -> Dict:

        score = 0.0
        breakdown = {}

        # ==========================================
        # 1. REQUIRED SKILLS (40)
        # ==========================================

        required = job.get("required_skills", {})
        candidate_skills = candidate.get("skill_stats", {})

        if required:

            matched = sum(
                1
                for skill in required.keys()
                if skill in candidate_skills
            )

            skills_score = (matched / len(required)) * 40

        else:
            skills_score = 40

        score += skills_score
        breakdown["required_skills"] = round(skills_score, 2)

        # ==========================================
        # 2. GITHUB LANGUAGES (20)
        # ==========================================

        preferred = job.get("preferred_skills", {})

        github_languages = {
            language.lower()
            for language in candidate.get("github_languages", [])
        }

        if preferred:

            matched = sum(
                1
                for language in preferred.keys()
                if language in github_languages
            )

            language_score = (matched / len(preferred)) * 20

        else:
            language_score = 20

        score += language_score
        breakdown["preferred_languages"] = round(language_score, 2)

        # ==========================================
        # 3. DSA EXPERIENCE (25)
        # ==========================================

        solved = candidate.get("total_solved", 0)

        if solved >= 500:
            dsa_score = 25

        elif solved >= 300:
            dsa_score = 20

        elif solved >= 200:
            dsa_score = 15

        elif solved >= 100:
            dsa_score = 10

        else:
            dsa_score = 5

        score += dsa_score
        breakdown["leetcode"] = dsa_score

        # ==========================================
        # 4. GITHUB EXPERIENCE (15)
        # ==========================================

        repos = candidate.get("repo_count", 0)
        stars = candidate.get("github_stars", 0)

        github_score = min(
            15,
            repos + (stars * 0.5)
        )

        score += github_score
        breakdown["github"] = round(github_score, 2)

        return {
            "match_score": round(score, 2),
            "breakdown": breakdown,
        }