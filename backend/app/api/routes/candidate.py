from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)

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

from backend.app.services.resume_service import (
    upload_resume_service,
    delete_resume_service,
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



#UPLOAD RESUME

@router.post(
    "/resume"
)
def upload_resume_route(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_candidate),
):
    return upload_resume_service(
        current_user.user_id,
        file,
    )

@router.delete(
    "/resume",
)
def delete_resume_route(
    current_user: UserResponse = Depends(get_current_candidate),
):

    return delete_resume_service(
        current_user.user_id
    )