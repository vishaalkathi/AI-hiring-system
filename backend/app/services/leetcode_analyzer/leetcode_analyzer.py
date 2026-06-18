from backend.app.services.base_analyzer import BaseAnalyzer
from .leetcode_api import fetch_leetcode_data
from .leet_feature_extractor import extract_features as extract_leet_features


class LeetCodeAnalyzer(BaseAnalyzer):

    def fetch_raw_data(self, username: str) -> dict:
        """
        Step 1: Pull raw LeetCode data
        """
        return fetch_leetcode_data(username)

    def extract_features(self, raw_data: dict) -> dict:
        """
        Step 2: Convert raw LeetCode data → features
        """

        if not raw_data:
            return {
                "error": "Failed to fetch data",
                "leetcode_score": 0
            }

        if "error" in raw_data:
            return {
                "error": raw_data["error"],
                "leetcode_score": 0
            }
        return extract_leet_features(raw_data)