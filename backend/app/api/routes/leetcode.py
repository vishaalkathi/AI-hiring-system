from fastapi import APIRouter, HTTPException,Depends

from backend.app.services.leetcode_analyzer.leetcode_analyzer import LeetCodeAnalyzer

from backend.app.api.dependencies import get_current_candidate

from backend.app.models.auth import UserResponse
from backend.app.models.leetcode import LeetCodeProfileCreate

from backend.app.services.leetcode_service import (
    sync_leetcode_profile_service,
    get_leetcode_profile_service,
    delete_leetcode_profile_service,
)
import logging

router = APIRouter()

'''
analyzer = LeetCodeAnalyzer()

@router.get("/leetcode-score/{username}")
def get_leetcode_score(username: str) -> dict:
    try:
        logging.info(f"[LeetCode API] Request received for LeetCode user: {username}")
        
        result = analyzer.analyze(username)

        if not result["features"] or result["features"].get("error"):
            logging.error(f"[LeetCode API] User not found: {username}")
            raise HTTPException(
                status_code=404,
                detail=f"LeetCode user '{username}' not found"
            )

        return {
            "status": "success",
            "data": result
        }
    except HTTPException:
        raise
    
    except Exception as e:
        logging.exception(f"[LeetCode API] Unexpected error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing the request"
        )
'''


@router.post("/candidate/leetcode")
def sync_leetcode_profile(

    leetcode: LeetCodeProfileCreate,

    current_user: UserResponse = Depends(get_current_candidate),

):
    return sync_leetcode_profile_service(
        current_user,
        leetcode.leetcode_username,
    )


@router.get("/candidate/leetcode")
def get_leetcode_profile_route(

    current_user: UserResponse = Depends(get_current_candidate),

):
    return get_leetcode_profile_service(current_user)


@router.delete("/candidate/leetcode")
def delete_leetcode_profile_route(

    current_user: UserResponse = Depends(get_current_candidate),

):
    return delete_leetcode_profile_service(current_user)