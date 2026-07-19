import math
from backend.app.models.scoring import Candidate

class ScoringEngine:

    def compute_score(self, candidate: Candidate) -> dict:

        f = candidate.combined_features
        github = candidate.github
        leetcode = candidate.leetcode

        #DSA SCORE

        dsa_score = min(math.log1p(f.total_solved) * 12, 50)

        #CONSISTENCY SCORE

        consistency_score = min(
            math.log1p(f.active_days) * 5 + f.streak * 0.5,
            20
        )

         # -------------------
        # SKILL SCORE (direct from leetcode)
        # -------------------
        skills = leetcode.skill_stats

        dp = skills.get("dynamic_programming", 0)
        graphs = skills.get("graph_theory", 0)
        greedy = skills.get("greedy", 0)

        skill_score = min(
            math.log1p(dp) * 2 +
            math.log1p(graphs) * 1.8 +
            math.log1p(greedy) * 1.5,
            20
        )

        # -------------------
        # GITHUB SCORE
        # -------------------
        github_score = min(
            math.log1p(f.repo_count) * 3 +
            math.log1p(f.github_stars) * 4 +
            math.log1p(github.followers) * 2,
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