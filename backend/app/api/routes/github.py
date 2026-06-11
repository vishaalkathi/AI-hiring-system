from fastapi import APIRouter, HTTPException
from backend.app.services.github_analyzer.github_analyzer import GitHubAnalyzer

import logging

router = APIRouter()

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