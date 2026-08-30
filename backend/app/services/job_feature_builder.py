import re
from fastapi import HTTPException, status

from backend.app.db.repositories.job_repository import (
    get_job_by_id,
)

from backend.app.models.features import JobFeatures

def parse_required_experience(value) -> float:

    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return max(0.0, float(value))

    text = str(value).strip().lower()

    if not text:
        return 0.0

    # --------------------------------------------------------
    # Fresher / entry-level
    # --------------------------------------------------------

    if any(word in text for word in [
        "fresher",
        "entry level",
        "entry-level",
        "no experience",
        "0 year",
        "0 years",
    ]):
        return 0.0

    # --------------------------------------------------------
    # Ranges
    # Handle BEFORE normal year extraction
    #
    # "3-5 years" -> 3.0
    # "2 to 4 years" -> 2.0
    # --------------------------------------------------------

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)",
        text
    )

    if range_match:
        return max(
            0.0,
            float(range_match.group(1))
        )

    # --------------------------------------------------------
    # Years + months
    #
    # "1 year 6 months" -> 1.5
    # "2 years" -> 2.0
    # --------------------------------------------------------

    year_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        text
    )

    month_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:months?|mos?)",
        text
    )

    years = (
        float(year_match.group(1))
        if year_match
        else 0.0
    )

    months = (
        float(month_match.group(1))
        if month_match
        else 0.0
    )

    if year_match or month_match:
        return max(
            0.0,
            years + (months / 12.0)
        )

    # --------------------------------------------------------
    # Plain number
    # --------------------------------------------------------

    number_match = re.search(
        r"\d+(?:\.\d+)?",
        text
    )

    if number_match:
        return float(number_match.group(0))

    return 0.0

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
        experience_required=parse_required_experience(
            job.get("experience_required")
        ),
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        status=job.get("status", "OPEN"),
    )