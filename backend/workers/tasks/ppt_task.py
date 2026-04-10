from workers.celery_app import celery_app
from workers.tasks.utils import sync_update_job
from storage.local_storage import save_json
from models.job import JobStatus
from ai_engine.pipelines.ppt_pipeline import run_ppt_pipeline
from workers.tasks.audio_tasks import generate_ppt_audio_subtask
from celery import group
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def generate_ppt_task(self, job_id: str, user_id: str, topic: str):
    """"
    Supercharged Main Execution Thread generating initial PPT natively, followed
    strictly by immediately spawning X detached concurrent group workers securely avoiding deadlocks.
    """
    logger.info(f"[Main PPT Pipeline Runner] Generation initialized onto Job {job_id} / '{topic}'")
    
    try:
        sync_update_job(job_id, JobStatus.processing, progress=10)
        
        # 40% signifies strict LLM query starting synchronously natively
        sync_update_job(job_id, JobStatus.processing, progress=40)
        
        # Execute absolute native logic
        pipeline_output = run_ppt_pipeline(job_id, topic)
        
        # Format Data Schema Mapping immediately into PSQL for frontend rendering while Audio spins up
        initial_result = {
            "topic": topic,
            "script_path": pipeline_output["paths"]["script"],
            "chunks_path": pipeline_output["paths"]["chunks"],
            "script": pipeline_output["script"]  
        }
        
        # Signal 60% completion natively proving Script JSON perfectly completed natively.
        sync_update_job(job_id, JobStatus.processing, progress=60, result=initial_result)
        
        # --- PARALLEL AUDIO DEPLOYMENT SEQUENCES ---
        slides = pipeline_output["script"].get("slides", [])
        total_slides = len(slides)
        
        if total_slides > 0:
            logger.info(f"Unleashing {total_slides} concurrent background Audio processes.")
            subtasks = [
                generate_ppt_audio_subtask.s(job_id, slide["slide_no"], slide.get("explanation", ""), total_slides) 
                for slide in slides
            ]
            # Detach Group fully natively bypassing main thread locks globally.
            group(subtasks).apply_async()
        else:
            # Fallback Native Resolution cleanly strictly mapped
            sync_update_job(job_id, JobStatus.completed, progress=100)

        return True # Resolves Main Task instantaneously allowing Workers CPU dominance optimally.

    except Exception as exc:
        logger.error(f"[Main Pipeline Structure] Catastrophic LLM Thread Error: {exc}", exc_info=True)
        sync_update_job(job_id, JobStatus.failed, error=str(exc))
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
