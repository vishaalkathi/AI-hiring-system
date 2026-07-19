from fastapi import HTTPException, status

from backend.app.db.repositories.candidate_repository import (
    create_candidate_profile,
    get_candidate_profile,
    update_candidate_profile,
    delete_candidate_profile,
)

from backend.app.models.candidate import (
    CandidateProfileCreate,
    CandidateProfileUpdate,
)

def create_profile(user_id: str, profile: CandidateProfileCreate):

    existing = get_candidate_profile(user_id)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Candidate profile already exists."
        )

    return create_candidate_profile(user_id, profile)

def get_profile(user_id: str):

    profile = get_candidate_profile(user_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found."
        )

    return profile

def update_profile(
    user_id: str,
    profile: CandidateProfileUpdate,
):

    existing = get_candidate_profile(user_id)

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found."
        )

    return update_candidate_profile(user_id, profile)

def delete_profile(user_id: str):

    deleted = delete_candidate_profile(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found."
        )

    return {
        "message": "Candidate profile deleted successfully."
    }