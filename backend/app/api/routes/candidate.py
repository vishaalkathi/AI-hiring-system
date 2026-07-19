from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_current_candidate

from backend.app.models.auth import UserResponse
from backend.app.models.candidate import (
    CandidateProfileCreate,
    CandidateProfileUpdate,
    CandidateProfileResponse,
)

from backend.app.services.candidate_service import (
    create_profile,
    get_profile,
    update_profile,
    delete_profile,
)

router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"],
)

@router.post(
    "/profile",
    response_model=CandidateProfileResponse,
    status_code=201,
)
def create_candidate_profile_route(
    profile: CandidateProfileCreate,
    current_user: UserResponse = Depends(get_current_candidate),
):

    return create_profile(
        current_user.user_id,
        profile,
    )



@router.get(
    "/profile",
    response_model=CandidateProfileResponse,
)
def get_candidate_profile_route(
    current_user: UserResponse = Depends(get_current_candidate),
):

    return get_profile(current_user.user_id)



@router.put(
    "/profile",
    response_model=CandidateProfileResponse,
)
def update_candidate_profile_route(
    profile: CandidateProfileUpdate,
    current_user: UserResponse = Depends(get_current_candidate),
):

    return update_profile(
        current_user.user_id,
        profile,
    )


@router.delete("/profile")
def delete_candidate_profile_route(
    current_user: UserResponse = Depends(get_current_candidate),
):

    return delete_profile(current_user.user_id)