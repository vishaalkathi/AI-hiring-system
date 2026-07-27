from fastapi import APIRouter, HTTPException
from backend.app.services.candidate_pipeline import CandidatePipeline
from backend.app.services.job_matching_engine import JobMatchingEngine
from backend.app.models.features import JobFeatures

router = APIRouter()

@router.post("/match/{username}")
def match_candidate(username: str, job: JobFeatures):

    service = CandidateService()
    candidate = service.build_candidate(username)

    engine = JobMatchingEngine()
    match = engine.compute_match(candidate, job)

    return {
        "status": "success",
        "data": {
            "username": username,
            "job": job.dict(),
            "match": match
        }
    }