from backend.app.services.base_analyzer import BaseAnalyzer
from .leetcode_api import fetch_leetcode_data

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
        # Placeholder for actual feature extraction logic
        return {
            "features": raw_data  # In real implementation, this would be processed features
        }