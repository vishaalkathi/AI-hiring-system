from fastapi import APIRouter, HTTPException

from backend.app.services.candidate_service import CandidateService
from backend.app.services.scoring_engine_v1 import ScoringEngine

from backend.app.models.candidate import Candidate

router = APIRouter()

@router.get("/candidate/{username}")
def get_candidate(username: str):

    try:
        service = CandidateService()
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