from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from models.user import User
from models.job import JobType
from schemas.job import JobCreate
from services import job_service

async def handle_create_job(db: AsyncSession, current_user: User, job_type: JobType, job_in: JobCreate):
    return await job_service.create_job(db, current_user.id, job_type, job_in)

async def handle_get_job(db: AsyncSession, current_user: User, job_id: UUID):
    return await job_service.get_job_status(db, job_id, current_user.id)
