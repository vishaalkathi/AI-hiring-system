from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_current_employer

from backend.app.models.auth import UserResponse
from backend.app.models.employer import (
    EmployerProfileCreate,
    EmployerProfileUpdate,
    EmployerProfileResponse,
)

from backend.app.services.employer_service import (
    create_profile,
    get_profile,
    update_profile,
    delete_profile,
)

router = APIRouter(
    prefix="/employer",
    tags=["Employer"],
)

@router.post(
    "/profile",
    response_model=EmployerProfileResponse,
)
def create_employer_profile_route(
    profile: EmployerProfileCreate,
    current_user: UserResponse = Depends(get_current_employer),
):

    return create_profile(
        current_user.user_id,
        profile,
    )



@router.get(
    "/profile",
    response_model=EmployerProfileResponse,
)
def get_employer_profile_route(
    current_user: UserResponse = Depends(get_current_employer),
):

    return get_profile(
        current_user.user_id,
    )



@router.put(
    "/profile",
    response_model=EmployerProfileResponse,
)
def update_employer_profile_route(
    profile: EmployerProfileUpdate,
    current_user: UserResponse = Depends(get_current_employer),
):

    return update_profile(
        current_user.user_id,
        profile,
    )



@router.delete("/profile")
def delete_employer_profile_route(
    current_user: UserResponse = Depends(get_current_employer),
):

    return delete_profile(
        current_user.user_id,
    )