from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.user import User
from models.job import JobType
from schemas.job import JobResponse, JobCreate
from api.deps import get_current_user
from controllers import job_controller

router = APIRouter()

@router.post("/{type}", response_model=JobResponse)
async def create_job(
    type: JobType = Path(..., title="The type of job to generate (ppt, podcast, video)"),
    job_in: JobCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a new job with Topic and pushes it to the Celery queue instantly."""
    return await job_controller.handle_create_job(db, current_user, type, job_in)
