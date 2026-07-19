from fastapi import HTTPException, status

from backend.app.models.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
)

from backend.app.db.repositories.user_repository import (
    create_user,
    get_user_by_email,
)

from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

def register(user: UserRegister) -> UserResponse:

    existing = get_user_by_email(user.email)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    password_hash = hash_password(user.password)

    created_user = create_user(
        name = user.name,
        email = user.email,
        password_hash = password_hash,
        role = user.role.value
    )

    return UserResponse(**created_user)

def login(user: UserLogin) -> TokenResponse:

    existing = get_user_by_email(user.email)

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(user.password,existing["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )
    
    token = create_access_token(
        existing["user_id"]
    )

    return TokenResponse(
        access_token=token
    )