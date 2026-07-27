from backend.app.services.registry import AnalyzerRegistry
from backend.app.services.candidate_feature_builder import build_candidate_features


class CandidatePipeline:

    def build_candidate(self, username: str):

        registry = AnalyzerRegistry()
        raw_data = registry.run_all(username)

        aggregator = build_candidate_features()
        candidate = aggregator.aggregate(
            raw_data.get("github", {}),
            raw_data.get("leetcode", {})
        )

        return candidate