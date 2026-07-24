from fastapi import HTTPException, status

from backend.app.db.repositories.application_repository import (
    create_application,
    application_exists,
    get_candidate_applications,
    get_job_applications,
    get_application_by_id,
    update_application_status
)

from backend.app.db.repositories.job_repository import get_job_by_id

from backend.app.models.application import (
    ApplicationUpdate,
    ApplicationResponse
)

from backend.app.models.auth import UserResponse

def create_application_service(
        current_user: UserResponse,
        job_id: str,
):
    job = get_job_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    if application_exists(
        str(current_user.user_id),
        job_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job.",
        )

    return create_application(
        str(current_user.user_id),
        job_id,
    )

def get_my_applications_service(
    current_user: UserResponse,
):
    return get_candidate_applications(
        str(current_user.user_id)
    )


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

    if str(job["employer_user_id"]) != str(current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these applications.",
        )

    return get_job_applications(job_id)


def update_application_status_service(
    application_id: str,
    application: ApplicationUpdate,
    current_user: UserResponse,
):
    existing_application = get_application_by_id(application_id)

    if not existing_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    job = get_job_by_id(str(existing_application["job_id"]))

    if str(job["employer_user_id"]) != str(current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    return update_application_status(
        application_id,
        application,
    )