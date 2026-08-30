from fastapi import APIRouter, HTTPException

from backend.app.services.candidate_feature_builder import (
    build_candidate_features,
)

from backend.app.services.job_feature_builder import (
    build_job_features,
)

from backend.app.services.job_matching_engine import (
    MatchingEngine,
)


router = APIRouter()


@router.post("/match/{user_id}/{job_id}")
def match_candidate(
    user_id: str,
    job_id: str,
):

    try:

        # Build candidate features from database
        candidate = build_candidate_features(
            user_id
        )

        # Build job features from database
        job = build_job_features(
            job_id
        )

        # Calculate match
        engine = MatchingEngine()

        match = engine.calculate_match_score(
            candidate.model_dump(),
            job.model_dump(),
        )

        return {
            "status": "success",
            "data": {
                "user_id": user_id,
                "job_id": job_id,
                "match": match,
            },
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )