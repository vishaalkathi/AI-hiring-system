from fastapi import HTTPException, status

from backend.app.db.repositories.application_repository import (
    create_application,
    application_exists,
    get_candidate_applications,
    get_job_applications,
    get_application_by_id,
    update_application_status,
)

from backend.app.db.repositories.job_repository import (
    get_job_by_id,
)

from backend.app.db.repositories.candidate_repository import (
    get_candidate_profile,
)

from backend.app.models.application import (
    ApplicationUpdate,
)

from backend.app.models.auth import UserResponse

from backend.app.services.candidate_feature_builder import (
    build_candidate_features,
)

from backend.app.services.job_feature_builder import (
    build_job_features,
)

from backend.app.services.job_matching_engine import (
    JobMatchingEngine,
)


# ============================================================
# CREATE APPLICATION
# ============================================================

def create_application_service(
    current_user: UserResponse,
    job_id: str,
):
    candidate_user_id = str(current_user.user_id)

    # --------------------------------------------------------
    # Check job exists
    # --------------------------------------------------------

    job = get_job_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # --------------------------------------------------------
    # Check candidate profile exists
    # --------------------------------------------------------

    candidate_profile = get_candidate_profile(
        candidate_user_id
    )

    if not candidate_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    # --------------------------------------------------------
    # Prevent duplicate application
    # --------------------------------------------------------

    if application_exists(
        candidate_user_id,
        job_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied for this job.",
        )

    # --------------------------------------------------------
    # Build candidate features
    # --------------------------------------------------------

    candidate_features = build_candidate_features(
        candidate_user_id
    )

    # --------------------------------------------------------
    # Build job features
    # --------------------------------------------------------

    job_features = build_job_features(
        job_id
    )

    # --------------------------------------------------------
    # Calculate ML match
    # --------------------------------------------------------

    engine = JobMatchingEngine()

    matching = engine.compute_match(
        candidate_features.model_dump(),
        job_features.model_dump(),
    )

    # --------------------------------------------------------
    # Save application + immutable resume snapshot
    # --------------------------------------------------------

    application = create_application(
        candidate_user_id=candidate_user_id,
        job_id=job_id,

        match_score=matching["match_score"],

        resume_snapshot=(
            candidate_features.resume
        ),

        parsed_role_snapshot=(
            candidate_features.candidate_role
        ),

        parsed_skills_snapshot=(
            candidate_features.candidate_skills
        ),

        parsed_experience_snapshot=(
            candidate_features.candidate_experience
        ),
    )

    # --------------------------------------------------------
    # Return application + matching information
    # --------------------------------------------------------

    return {
        "application": application,
        "matching": matching,
    }


# ============================================================
# GET MY APPLICATIONS
# ============================================================

def get_my_applications_service(
    current_user: UserResponse,
):
    return get_candidate_applications(
        str(current_user.user_id)
    )


# ============================================================
# GET APPLICATIONS FOR A JOB
# ============================================================

def get_job_applications_service(
    job_id: str,
    current_user: UserResponse,
):
    job = get_job_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Only the employer who owns the job can view applications

    if str(job["employer_user_id"]) != str(
        current_user.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these applications.",
        )

    return get_job_applications(job_id)


# ============================================================
# UPDATE APPLICATION STATUS
# ============================================================

def update_application_status_service(
    application_id: str,
    application: ApplicationUpdate,
    current_user: UserResponse,
):
    existing_application = get_application_by_id(
        application_id
    )

    if not existing_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    job = get_job_by_id(
        str(existing_application["job_id"])
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Only the employer who owns the job can update status

    if str(job["employer_user_id"]) != str(
        current_user.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    return update_application_status(
        application_id,
        application,
    )
