from fastapi import APIRouter,Depends

from backend.app.api.dependencies import (
    get_current_candidate,
    get_current_employer,
)

from backend.app.models.application import (
    ApplicationResponse,
    ApplicationUpdate
)

from backend.app.models.auth import UserResponse

from backend.app.services.application_service import (
    create_application_service,
    get_my_applications_service,
    get_job_applications_service,
    update_application_status_service,
)

router = APIRouter()

@router.post("/jobs/{job_id}/apply")
def apply_for_job(
    job_id: str,
    current_user: UserResponse = Depends(get_current_candidate),
):
    return create_application_service(
        current_user,
        job_id,
    )

@router.get("/applications/me")
def get_my_applications(
    current_user: UserResponse = Depends(get_current_candidate),
):
    return get_my_applications_service(
        current_user,
    )

@router.get("/jobs/{job_id}/applications")
def get_job_applications_route(
    job_id: str,
    current_user: UserResponse = Depends(get_current_employer)
):
    return get_job_applications_service(
        job_id,
        current_user
    )

@router.patch("/applications/{application_id}") #To change the status of an application
def update_application_route(
    application_id: str,
    application: ApplicationUpdate,
    current_user: UserResponse = Depends(get_current_employer),
):
    return update_application_status_service(
        application_id,
        application,
        current_user,
    )