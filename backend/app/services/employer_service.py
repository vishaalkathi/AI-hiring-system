from fastapi import HTTPException

from backend.app.db.repositories.employer_repository import (
    create_employer_profile,
    get_employer_profile,
    update_employer_profile,
    delete_employer_profile,
)

from backend.app.models.employer import (
    EmployerProfileCreate,
    EmployerProfileUpdate,
    EmployerProfileResponse,
)


def create_profile(
    user_id: str,
    profile: EmployerProfileCreate,
):

    created = create_employer_profile(user_id, profile)

    return EmployerProfileResponse(**created)


def get_profile(user_id: str):

    profile = get_employer_profile(user_id)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Employer profile not found",
        )

    return EmployerProfileResponse(**profile)


def update_profile(
    user_id: str,
    profile: EmployerProfileUpdate,
):

    updated = update_employer_profile(user_id, profile)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Employer profile not found",
        )

    return EmployerProfileResponse(**updated)


def delete_profile(user_id: str):

    profile = get_employer_profile(user_id)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Employer profile not found",
        )

    delete_employer_profile(user_id)

    return {
        "message": "Employer profile deleted successfully"
    }