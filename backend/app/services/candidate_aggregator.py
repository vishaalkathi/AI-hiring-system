class CandidateAggregator:
    def aggregate(self, github_features: dict, leetcode_features: dict) -> dict:

        combined = {}

        #store raw sources
        combined["github"] = github_features
        combined["leetcode"] = leetcode_features

        #combine into unified feature set
        combined_features = {}

        # LeetCode signals
        combined_features["total_solved"] = leetcode_features.get("features", {}).get("total_solved", 0)
        combined_features["streak"] = leetcode_features.get("features", {}).get("streak", 0)
        combined_features["active_days"] = leetcode_features.get("features", {}).get("active_days", 0)

        combined_features["skill_stats"] = leetcode_features.get("features", {}).get("skill_stats", {})
        combined_features["language_diversity"] = leetcode_features.get("features", {}).get("language_diversity", 0)

        # GitHub signals
        combined_features["repo_count"] = github_features.get("features", {}).get("public_repos", 0)
        combined_features["github_stars"] = github_features.get("features", {}).get("total_stars", 0)

        combined["combined_features"] = combined_features

        return combined