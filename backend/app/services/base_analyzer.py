from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    """
    Shared interface for all coding profile analyzers
    (GitHub, LeetCode, Codeforces, etc.)
    """

    @abstractmethod
    def fetch_raw_data(self, username: str) -> dict:
        """
        Step 1: Fetch raw data from external source
        """
        pass

    @abstractmethod
    def extract_features(self, raw_data: dict) -> dict:
        """
        Step 2: Convert raw data into clean ML-ready features
        """
        pass

    def analyze(self, username: str) -> dict:
        """
        Template method:
        Standard pipeline for ALL platforms
        """
        raw_data = self.fetch_raw_data(username)
        features = self.extract_features(raw_data)

        return {
            "username": username,
            "features": features
        }