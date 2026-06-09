from fastapi import APIRouter, HTTPException
from backend.app.services.github_analyzer.github_api import get_user, get_repos
from backend.app.services.github_analyzer.repo_analyzer import extract_features
from backend.app.services.github_analyzer.metrics import github_score
import logging

router = APIRouter()

@router.get("/github-score/{username}")
def get_github_score(username: str) -> dict:
    try:
        logging.info(f"[Github API] Request received for GitHub user: {username}")
        user_data = get_user(username)

        if not user_data:
            logging.error(f"[Github API] GitHub user '{username}' not found")
            raise HTTPException(
                status_code=404,
                detail=f"GitHub user '{username}' not found"
            )
        
        logging.info(f"[Github API] User data fetched for {username}")

        repos = get_repos(username) or []
        logging.info(f"[Github API] Repositories fetched for {username}: {len(repos)} repos found")

        features = extract_features(user_data, repos)
        logging.info(f"[Github API] Features extracted for {username}: {features}")

        score = github_score(features)
        logging.info(f"[Github API] Calculated GitHub score for {username}: {score}")

        return {
            "status": "success",
            "data": {
                "username": username,
                "github_score": score,
                "features": features
            }
        }
    except HTTPException:
        raise
    
    except Exception as e:
        logging.exception(f"[Github API] Unexpected error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing the request"
        )