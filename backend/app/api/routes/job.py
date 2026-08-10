from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_current_employer

from backend.app.models.auth import UserResponse
from backend.app.models.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
)

from backend.app.services.job_service import (
    create_job_service,
    get_job_service,
    get_employer_jobs_service,
    update_job_service,
    delete_job_service,
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job_route(
    job: JobCreate,
    current_user: UserResponse = Depends(get_current_employer),
):

    return create_job_service(
        current_user.user_id,
        job,
    )



@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job_route(
    job_id: str,
):

    return get_job_service(job_id)



@router.get(
    "/me/all",
    response_model=list[JobResponse],
)
def get_my_jobs_route(
    current_user: UserResponse = Depends(get_current_employer),
):

    return get_employer_jobs_service(
        current_user.user_id
    )



@router.put(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job_route(
    job_id: str,
    job: JobUpdate,
    current_user: UserResponse = Depends(get_current_employer),
):

    return update_job_service(
        job_id,
        job,
    )



@router.delete(
    "/{job_id}",
)
def delete_job_route(
    job_id: str,
    current_user: UserResponse = Depends(get_current_employer),
):

    return delete_job_service(job_id)

from backend.app.services.job_feature_builder import build_job_features

@router.get("/{job_id}/features")
def get_job_features(
    job_id: str,
):
    return build_job_features(job_id)