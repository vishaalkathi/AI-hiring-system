from backend.app.services.registry import AnalyzerRegistry
from backend.app.services.candidate_aggregator import CandidateAggregator


class CandidateService:

    def build_candidate(self, username: str):

        registry = AnalyzerRegistry()
        raw_data = registry.run_all(username)

        aggregator = CandidateAggregator()
        candidate = aggregator.aggregate(
            raw_data.get("github", {}),
            raw_data.get("leetcode", {})
        )

        return candidate