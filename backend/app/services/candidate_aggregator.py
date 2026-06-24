class CandidateAggregator:
    def aggregate(self, github_raw: dict, leetcode_raw: dict) -> dict:

        # -------------------------
        # NORMALIZE INPUT FIRST
        # -------------------------
        github = github_raw.get("features", github_raw)
        leetcode = leetcode_raw.get("features", leetcode_raw)

        # -------------------------
        # RAW STORAGE (optional debug)
        # -------------------------
        combined = {
            "github": github,
            "leetcode": leetcode
        }

        # -------------------------
        # COMBINED FEATURES (ML VECTOR)
        # -------------------------
        combined_features = {
            # LeetCode signals
            "total_solved": leetcode.get("total_solved", 0),
            "streak": leetcode.get("streak", 0),
            "active_days": leetcode.get("active_days", 0),

            "skill_stats": leetcode.get("skill_stats", {}),
            "language_diversity": leetcode.get("language_diversity", 0),

            # GitHub signals
            "repo_count": github.get("public_repos", 0),
            "github_stars": github.get("total_stars", 0),
            "github_followers": github.get("followers", 0),
        }

        combined["combined_features"] = combined_features

        return combined