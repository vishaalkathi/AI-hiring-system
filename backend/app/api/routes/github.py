from fastapi import APIRouter, HTTPException,Depends
from backend.app.services.github_analyzer.github_analyzer import GitHubAnalyzer


from backend.app.api.dependencies import get_current_candidate

from backend.app.models.auth import UserResponse
from backend.app.models.github import GitHubProfileCreate

from backend.app.services.github_service import (
    sync_github_profile_service,
    get_github_profile_service,
    delete_github_profile_service,
)
import logging

router = APIRouter()


'''
-------------------
OLD GITHUB API
-------------------

analyzer = GitHubAnalyzer()

@router.get("/github-score/{username}")
def get_github_score(username: str) -> dict:
    try:
        logging.info(f"[Github API] Request received for GitHub user: {username}")
        
        result = analyzer.analyze(username)

        if not result["features"] or result["features"].get("error"):
            logging.error(f"[GitHub API] User not found: {username}")
            raise HTTPException(
                status_code=404,
                detail=f"GitHub user '{username}' not found"
            )

        return {
            "status": "success",
            "data": result
        }
    except HTTPException:
        raise
    
    except Exception as e:
        logging.exception(f"[Github API] Unexpected error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing the request"
        )
'''


@router.post("/candidate/github")
def sync_github_profile(
    github: GitHubProfileCreate,
    current_user: UserResponse = Depends(get_current_candidate),
):
    return sync_github_profile_service(
        current_user,
        github.github_username,
    )


@router.get("/candidate/github")
def get_github_profile_route(
    current_user: UserResponse = Depends(get_current_candidate),
):
    return get_github_profile_service(current_user)


@router.delete("/candidate/github")
def delete_github_profile_route(
    current_user: UserResponse = Depends(get_current_candidate),
):
    return delete_github_profile_service(current_user)