import math

class JobMatchingEngine:

    def compute_match(self, candidate: dict, job):

        f = candidate.get("combined_features", {})

        # DSA FIT
        total_solved = f.get("total_solved", 0)
        dsa_fit = min(math.log1p(total_solved) * 10, 50)

        # CONSISTENCY
        streak = f.get("streak", 0)
        active_days = f.get("active_days", 0)

        consistency_fit = min(
            math.log1p(active_days) * 5 + streak * 0.5,
            20
        )

        # SKILL FIT
        skill_stats = f.get("skill_stats", {})

        dp = skill_stats.get("dynamic_programming", 0)
        graphs = skill_stats.get("graph_theory", 0)
        greedy = skill_stats.get("greedy", 0)

        skill_score = min(
            math.log1p(dp) * 2 +
            math.log1p(graphs) * 1.8 +
            math.log1p(greedy) * 1.5,
            20
        )

        # GITHUB FIT
        repo_count = f.get("repo_count", 0)
        stars = f.get("github_stars", 0)

        github_fit = min(
            math.log1p(repo_count) * 3 +
            math.log1p(stars) * 4,
            10
        )

        # FINAL SCORE
        final_score = dsa_fit + consistency_fit + skill_score + github_fit

        return {
            "match_score": round(final_score, 2),
            "fit": self.get_fit(final_score),
            "breakdown": {
                "dsa_fit": round(dsa_fit, 2),
                "skill_score": round(skill_score, 2),
                "github_fit": round(github_fit, 2)
            }
        }

    def get_fit(self, score: float):
        if score > 80:
            return "Strong Match"
        elif score > 60:
            return "Good Match"
        elif score > 40:
            return "Average Match"
        else:
            return "Weak Match"