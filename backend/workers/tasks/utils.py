import asyncio
from sqlalchemy.future import select
from db.database import AsyncSessionLocal
from models.job import Job, JobStatus
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def _update_job_status(job_id: str, status: JobStatus, progress: int = None, result: dict = None, error: str = None):
    async with AsyncSessionLocal() as session:
        qs = await session.execute(select(Job).where(Job.job_id == job_id))
        job = qs.scalar_one_or_none()
        if job:
            job.status = status
            job.updated_at = datetime.utcnow()
            if progress is not None:
                job.progress = progress
            if result is not None:
                if job.result is None:
                    job.result = result
                else:
                    if isinstance(job.result, dict) and isinstance(result, dict):
                        new_res = dict(job.result)
                        new_res.update(result)
                        job.result = new_res
                    else:
                        job.result = result
            if error is not None:
                job.error = error
            await session.commit()
            logger.info(f"DB Sync success: Job {job_id} -> {status.value} (Progress: {progress}%)")

def sync_update_job(job_id: str, status: JobStatus, progress: int = None, result: dict = None, error: str = None):
    """
    Synchronously runs accurate native database status logic strictly ensuring the connection
    resolves from inside Celery independent runtime pools safely blocking.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(_update_job_status(job_id, status, progress, result, error))
