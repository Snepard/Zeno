from fastapi import APIRouter
from api.routes.auth import router as auth_router
from api.routes.generate import router as generate_router
from api.routes.job import router as job_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(generate_router, prefix="/generate", tags=["generate"], responses={401: {"description": "Unauthorized"}})
api_router.include_router(job_router, prefix="/job", tags=["job"], responses={401: {"description": "Unauthorized"}})
