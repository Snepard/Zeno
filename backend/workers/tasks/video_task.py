from workers.celery_app import celery_app
from workers.tasks.utils import sync_update_job
from ai_engine.video.video_pipeline import generate_master_video
from models.job import JobStatus
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, queue="gpu")
def generate_lecture_video(self, job_id: str):
    """
    High Priority Render Worker mapped explicitly traversing strictly HW limits natively globally protecting API.
    """
    logger.info(f"Executing deep Video Rendering strictly on Dedicated HW Node dynamically: Job {job_id}")
    try:
        # Pre-execution limits natively mapped protecting sequence bounds perfectly (40% - 60% - 80%)
        sync_update_job(job_id, JobStatus.processing, progress=80) 
        
        # Audio aggregation perfectly mapping sequential timelines intelligently 
        res = generate_master_video(job_id)
        
        # We hook Lipsync processing entirely traversing boundaries explicitly queuing sequentially natively seamlessly
        from workers.tasks.lipsync_task import generate_lipsync_hook
        generate_lipsync_hook.delay(job_id, res["full_audio"])
        
        return True
    except Exception as e:
        logger.error(f"Video Pipeline completely fatally faulted natively mapping sequence bounds: {e}", exc_info=True)
        sync_update_job(job_id, JobStatus.failed, error=str(e))
