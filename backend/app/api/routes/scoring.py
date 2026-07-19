from fastapi import APIRouter, HTTPException

from backend.app.services.candidate_pipeline import CandidatePipeline
from backend.app.services.scoring_engine_v1 import ScoringEngine

from backend.app.models.scoring import Candidate

router = APIRouter()

@router.get("/score/{username}")
def get_candidate(username: str):

    try:
        service = CandidatePipeline()
        candidate = service.build_candidate(username)

        scorer = ScoringEngine()
        score = scorer.compute_score(candidate)

        return {
            "status": "success",
            "data": {
                "username": username,
                "candidate": candidate,
                "score": score
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     