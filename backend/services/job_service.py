from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from fastapi import HTTPException
from models.job import Job, JobType, JobStatus
from schemas.job import JobCreate
from workers.tasks.ppt_task import generate_ppt_task
from workers.tasks.podcast_task import generate_podcast_task
import logging

logger = logging.getLogger(__name__)

async def create_job(db: AsyncSession, user_id: UUID, job_type: JobType, job_in: JobCreate) -> Job:
    # 1. Create Job in DB and setup parameters instantly capturing 0ms API response constraint
    db_job = Job(
        user_id=user_id,
        type=job_type,
        status=JobStatus.queued,
        progress=0,
        result={"topic": job_in.topic}
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    
    # 2. Dispatch cleanly to distinct Celery workers depending on JobType
    if job_type == JobType.ppt:
        generate_ppt_task.delay(str(db_job.job_id), str(user_id), job_in.topic)
    elif job_type == JobType.podcast:
        generate_podcast_task.delay(str(db_job.job_id), str(user_id), job_in.topic)
    else:
        # Fallback (e.g. video logic) 
        pass
    
    return db_job

async def get_job_status(db: AsyncSession, job_id: UUID, user_id: UUID) -> Job:
    result = await db.execute(select(Job).where(Job.job_id == job_id, Job.user_id == user_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return job
