from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.app.core.security import decode_access_token
from backend.app.db.repositories.user_repository import get_user_by_id

from backend.app.models.auth import UserResponse
from backend.app.models.enums import UserRole

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)                                       #it reads to authorization header that the api returns and extracts the token string and stores that

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    user_id = decode_access_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid authentication credentials"
        )
    
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid user credentials"
        )

    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        name=user["name"],
        role=user["role"],
    )

def get_current_candidate(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Candidate access only"
        )
    
    return current_user

def get_current_employer(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.EMPLOYER:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Employer access only"
        )
    
    return current_user