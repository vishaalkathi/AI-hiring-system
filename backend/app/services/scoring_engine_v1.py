import math

class ScoringEngine:

    def compute_score(self, candidate: dict) -> dict:

        f = candidate["combined_features"]

        #DSA SCORE

        total_solved = f.get("total_solved", 0)
        dsa_score = min(math.log1p(total_solved) * 12, 50)

        #CONSISTENCY SCORE

        streak = f.get("streak", 0)
        active_days = f.get("active_days", 0)

        consistency_score = min(math.log1p(active_days) * 5 + streak * 0.5, 20)

        #SKILL DEPTH SCORE

        skill_stats = f.get("skill_stats", {})

        dp = skill_stats.get("dynamic_programming", 0)
        graphs = skill_stats.get("graph_theory", 0)
        greedy = skill_stats.get("greedy_algorithms", 0)

        skill_score = min(
            (
                math.log1p(dp) * 2 +
                math.log1p(graphs) * 1.8 +
                math.log1p(greedy) * 1.5
            ),
            20
        )

        # 4. GITHUB SCORE

        repo_count = f.get("repo_count", 0)
        stars = f.get("github_stars", 0)
        followers = f.get("github_followers", 0)

        github_score = min(
            math.log1p(repo_count) * 3 +
            math.log1p(stars) * 4 +
            math.log1p(followers) * 2,
            10
        )
        # -------------------
        # FINAL SCORE
        # -------------------
        final_score = (
            dsa_score +
            consistency_score +
            skill_score +
            github_score
        )

        return {
            "final_score": round(final_score, 2),
            "verdict": self.get_verdict(final_score),
            "breakdown": {
                "dsa_score": round(dsa_score, 2),
                "consistency_score": round(consistency_score, 2),
                "skill_score": round(skill_score, 2),
                "github_score": round(github_score, 2)
            }
        }

    def get_verdict(self,score: float) -> str:

        if score > 80:
            return "Strong Candidate"
        elif score > 60:
            return "Good Candidate"
        elif score > 40:
            return "Average Candidate"
        else:
            return "Needs Improvement"