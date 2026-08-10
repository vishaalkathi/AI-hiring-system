from fastapi import HTTPException, status

from backend.app.db.repositories.job_repository import (
    get_job_by_id,
)

from backend.app.models.features import JobFeatures


def build_job_features(job_id: str) -> JobFeatures:
    """
    Build a matching-ready feature vector from
    a persisted job.
    """

    job = get_job_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    required_skills = job.get("required_skills") or {}
    preferred_skills = job.get("preferred_skills") or []

    return JobFeatures(
        job_id=str(job["job_id"]),
        title=job["title"],
        description=job["description"],
        location=job.get("location"),
        employment_type=job.get("employment_type"),
        experience_required=job.get(
            "experience_required"
        ),
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        status=job.get("status", "OPEN"),
    )