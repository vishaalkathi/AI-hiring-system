from fastapi import APIRouter, HTTPException

from backend.app.services.registry import AnalyzerRegistry
from backend.app.services.candidate_aggregator import CandidateAggregator
from backend.app.services.scoring_engine_v1 import ScoringEngine

from backend.app.models.candidate import Candidate

router = APIRouter()

@router.get("/candidate/{username}")
def get_candidate(username: str):

    try:
        # -------------------------
        # 1. RUN ALL ANALYZERS
        # -------------------------
        registry = AnalyzerRegistry()
        raw_data = registry.run_all(username)

        # -------------------------
        # 2. AGGREGATE
        # -------------------------
        aggregator = CandidateAggregator()
        candidate_raw = aggregator.aggregate(
            raw_data.get("github", {}),
            raw_data.get("leetcode", {})
        )

        # convert dict → Pydantic model
        candidate = Candidate(
            username=username,
            github=candidate_raw.get("github", {}),
            leetcode=candidate_raw.get("leetcode", {}),
            combined_features=candidate_raw.get("combined_features", {})
        )

        # -------------------------
        # 3. SCORE
        # -------------------------
        scorer = ScoringEngine()
        score_result = scorer.compute_score(candidate)

        # -------------------------
        # 4. RESPONSE
        # -------------------------
        return {
            "status": "success",
            "data": {
                "username": username,
                "candidate": candidate,
                "score": score_result
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     