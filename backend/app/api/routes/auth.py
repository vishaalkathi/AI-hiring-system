from fastapi import APIRouter,Depends

from backend.app.models.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)

from backend.app.services.auth_service import (
    register,
    login
)

from backend.app.api.dependencies import (
    get_current_user,
    get_current_candidate,
    get_current_employer
)

router = APIRouter(
    prefix="/auth",
    tags = ["Authentication"]
)

@router.post("/register",response_model=UserResponse,status_code=201)
def register_user(user: UserRegister):
    return register(user)

@router.post("/login",response_model=TokenResponse)
def login_user(user:UserLogin):
    return login(user)

@router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/candidate-test")
def candidate_test(current_user = Depends(get_current_candidate)):
    return {
        "message" : "Welcome Candidate",
        "user" : current_user
    }

@router.get("/employer-test")
def employer_test(
    current_user = Depends(get_current_employer)
):
    return {
        "message": "Welcome Employer!",
        "user": current_user
    }