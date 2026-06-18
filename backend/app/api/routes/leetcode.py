from fastapi import APIRouter, HTTPException
from backend.app.services.leetcode_analyzer.leetcode_analyzer import LeetCodeAnalyzer

import logging

router = APIRouter()

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