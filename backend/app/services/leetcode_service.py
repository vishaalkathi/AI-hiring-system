from fastapi import HTTPException, status

from backend.app.models.auth import UserResponse

from backend.app.services.leetcode_analyzer.leetcode_analyzer import LeetCodeAnalyzer

from backend.app.db.repositories.leetcode_repository import (
    upsert_leetcode_profile,
    get_leetcode_profile,
    delete_leetcode_profile,
)

analyzer = LeetCodeAnalyzer()


def sync_leetcode_profile_service(
    current_user: UserResponse,
    leetcode_username: str,
):

    result = analyzer.analyze(leetcode_username)

    features = result.get("features")

    if not features or features.get("error"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LeetCode user not found.",
        )

    return upsert_leetcode_profile(
        str(current_user.user_id),
        leetcode_username,
        features,
    )


def get_leetcode_profile_service(
    current_user: UserResponse,
):

    profile = get_leetcode_profile(str(current_user.user_id))

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LeetCode profile not found.",
        )

    return profile


def delete_leetcode_profile_service(
    current_user: UserResponse,
):

    profile = delete_leetcode_profile(str(current_user.user_id))

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LeetCode profile not found.",
        )

    return {
        "message": "LeetCode profile deleted successfully."
    }