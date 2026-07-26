from fastapi import HTTPException, status

from backend.app.models.auth import UserResponse

from backend.app.services.github_analyzer.github_analyzer import GitHubAnalyzer

from backend.app.db.repositories.github_repository import (
    upsert_github_profile,
    get_github_profile,
    delete_github_profile,
)


analyzer = GitHubAnalyzer()


def sync_github_profile_service(
    current_user: UserResponse,
    github_username: str,
):
    result = analyzer.analyze(github_username)

    features = result.get("features")

    if not features or features.get("error"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub user not found.",
        )

    return upsert_github_profile(
        str(current_user.user_id),
        github_username,
        features,
    )


def get_github_profile_service(
    current_user: UserResponse,
):
    profile = get_github_profile(str(current_user.user_id))

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub profile not found.",
        )

    return profile


def delete_github_profile_service(
    current_user: UserResponse,
):
    profile = delete_github_profile(str(current_user.user_id))

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub profile not found.",
        )

    return {
        "message": "GitHub profile deleted successfully."
    }

