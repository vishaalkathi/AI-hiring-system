from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.api.routes.github import router as github_router
from backend.app.api.routes.leetcode import router as leetcode_router
from backend.app.api.routes.scoring import router as scoring_router
from backend.app.api.routes.job_matching import router as job_matching_router
from backend.app.api.routes.auth import router as auth_router
from backend.app.db.connection import (initialize_database, close_database)
from backend.app.api.routes.candidate import router as candidate_router
from backend.app.api.routes.employer import router as employer_router
from backend.app.api.routes.job import router as job_router
from backend.app.api.routes.application import router as application_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()  #Run when FastAPI starts
    yield
    '''
    Everything before yield happens once before the server starts accepting requests.

    Everything after yield happens once when the server shuts down.
    '''
    close_database() #Run when FastAPI shuts down

app = FastAPI(lifespan = lifespan)

app.include_router(github_router, prefix="/api")
app.include_router(leetcode_router, prefix="/api")
app.include_router(scoring_router, prefix="/api")
app.include_router(job_matching_router, prefix="/api")
app.include_router(auth_router,prefix="/api")
app.include_router(candidate_router,prefix="/api",)
app.include_router(employer_router,prefix="/api",)
app.include_router(job_router,prefix="/api")
app.include_router(application_router,prefix="/api")


@app.get("/")
def root():
    return {"message": "AI Hiring System Backend Running"}