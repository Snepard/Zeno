from worker.celery_app import celery_app
import logging
import asyncio
from sqlalchemy.future import select
from db.database import AsyncSessionLocal
from models.job import Job, JobStatus

logger = logging.getLogger(__name__)

async def _update_job_status(job_id: str, status: JobStatus):
    """Helper method to update job statuses actively from database asynchronously."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Job).where(Job.job_id == job_id))
        job = result.scalar_one_or_none()
        if job:
            job.status = status
            await session.commit()

@celery_app.task(bind=True)
def process_generation_job(self, job_id: str, user_id: str, job_type: str):
    """
    Actual worker task for processing generation in true MVP async fashion.
    This safely executes outside the main web layer preventing blocking.
    """
    logger.info(f"Starting generation job {job_id} of type {job_type} for user {user_id}")
    
    # Mark operation as processing
    asyncio.run(_update_job_status(job_id, JobStatus.processing))
    
    try:
        # ---
        # 🧠 AI PIPELINE LOGIC INVOCATION GOES HERE
        # e.g PPT generation, Video generation, Podcast mapping
        # ---
        import time
        time.sleep(5) # Simulating heavy operation logic (audio rendering, clip mapping, etc).
        
        # Mark as strictly completed
        asyncio.run(_update_job_status(job_id, JobStatus.completed))
        return {"job_id": job_id, "status": "completed"}
    except Exception as e:
        logger.error(f"Job {job_id} miserably failed: {e}", exc_info=True)
        asyncio.run(_update_job_status(job_id, JobStatus.failed))
        raise e
