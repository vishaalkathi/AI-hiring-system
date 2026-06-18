from fastapi import FastAPI
from backend.app.api.routes.github import router as github_router
from backend.app.api.routes.leetcode import router as leetcode_router

app = FastAPI()
app.include_router(github_router, prefix="/api")
app.include_router(leetcode_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI Hiring System Backend Running"}