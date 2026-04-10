from workers.celery_app import celery_app
from workers.tasks.utils import sync_update_job
from storage.local_storage import save_json
from models.job import JobStatus
from ai_engine.pipelines.podcast_pipeline import run_podcast_pipeline
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def generate_podcast_task(self, job_id: str, user_id: str, topic: str):
    logger.info(f"[Podcast Task] Live generation started for {job_id} on '{topic}'")
    
    try:
        # Initial 10%
        sync_update_job(job_id, JobStatus.processing, progress=10)
        
        # Dialouge Generation starting indicator
        sync_update_job(job_id, JobStatus.processing, progress=40)
        
        # 100% genuine LLM mapping process blocking
        pipeline_output = run_podcast_pipeline(job_id, topic)
        
        # 70% indicate file execution finishing sequence
        sync_update_job(job_id, JobStatus.processing, progress=70)
        
        # Output JSON embedding 
        final_result = {
            "topic": topic,
            "script_path": pipeline_output["paths"]["script"],
            "chunks_path": pipeline_output["paths"]["chunks"],
            "script_preview": pipeline_output["script"],
            "audio_path": None # Still missing physical MP3 Audio generator (Text-to-Speech phase)
        }
        save_json(job_id, "metadata.json", final_result)
        
        # 100% PSQL success
        sync_update_job(job_id, JobStatus.completed, progress=100, result=final_result)
        logger.info(f"[Podcast Task] Fully executed LLM generating Job {job_id}")
        return final_result

    except Exception as exc:
        logger.error(f"[Podcast Task] Critical failure via LLM mapping {job_id}: {exc}", exc_info=True)
        sync_update_job(job_id, JobStatus.failed, error=str(exc))
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
