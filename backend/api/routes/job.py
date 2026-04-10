from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db.database import get_db
from models.user import User
from schemas.job import JobResponse
from api.deps import get_current_user
from controllers import job_controller

router = APIRouter()

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Returns the job status for the current user."""
    return await job_controller.handle_get_job(db, current_user, job_id)
