from fastapi import HTTPException, status

from backend.app.db.repositories.job_repository import (
    create_job,
    get_job_by_id,
    get_jobs_by_employer,
    update_job,
    delete_job,
)


def create_job_service(
    employer_user_id,
    job
):

    return create_job(
        employer_user_id,
        job.model_dump()
    )


def get_job_service(job_id):

    job = get_job_by_id(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return job


def get_employer_jobs_service(
    employer_user_id
):

    return get_jobs_by_employer(
        employer_user_id
    )


def update_job_service(
    job_id,
    employer_user_id,
    job
):

    existing_job = get_job_by_id(job_id)

    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if str(existing_job["employer_user_id"]) != str(employer_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to modify this job."
        )

    updated = update_job(
        job_id,
        job.model_dump(exclude_unset=True)
    )

    return updated


def delete_job_service(
    job_id,
    employer_user_id
):

    existing_job = get_job_by_id(job_id)

    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if str(existing_job["employer_user_id"]) != str(employer_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this job."
        )

    deleted = delete_job(job_id)

    return {
        "message": "Job deleted successfully"
    }
