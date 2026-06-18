from backend.app.services.base_analyzer import BaseAnalyzer
from .github_api import get_user, get_repos
from .git_feature_extractor import extract_features as extract_repo_features


class GitHubAnalyzer(BaseAnalyzer):

    def fetch_raw_data(self, username: str) -> dict:
        """
        Step 1: Pull raw GitHub data
        """
        user_data = get_user(username)
        repos = get_repos(username)

        return {
            "user": user_data,
            "repos": repos
        }

    def extract_features(self, raw_data: dict) -> dict:
        """
        Step 2: Convert raw GitHub data → features
        """

        user_data = raw_data["user"]
        repos = raw_data["repos"]

        if not user_data:
            return {
                "error": "User not found",
                "github_score": 0
            }

        features = extract_repo_features(user_data, repos)

        return {
            "features": features
        }