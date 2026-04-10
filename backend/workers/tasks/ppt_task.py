from workers.celery_app import celery_app
from workers.tasks.utils import sync_update_job
from storage.local_storage import save_json
from models.job import JobStatus
from ai_engine.pipelines.ppt_pipeline import run_ppt_pipeline
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def generate_ppt_task(self, job_id: str, user_id: str, topic: str):
    """
    Real celery task logic powering a live PPT via LLMs natively connected.
    Overrides the old mock logic entirely executing OpenAI/Gemini strictly via Pydantic parsing.
    """
    logger.info(f"[PPT Task] Live generation fully started for Job {job_id} on '{topic}'")
    
    try:
        # Step 1: Initialize status accurately (10%)
        sync_update_job(job_id, JobStatus.processing, progress=10)
        
        # Step 2: Push 40% indicating Active LLM Call Generation sequence starting
        sync_update_job(job_id, JobStatus.processing, progress=40)
        
        # Step 3: Run pipeline blocking call (Wait for full AI completion, Chunking, DB mapping natively)
        pipeline_output = run_ppt_pipeline(job_id, topic)
        
        # Step 4: 70% Flag ensuring script completely captured correctly
        sync_update_job(job_id, JobStatus.processing, progress=70)
        
        # Step 5: Assign final data layout accurately embedding the actual metadata locally for later usage (e.g WebSockets).
        final_result = {
            "topic": topic,
            "script_path": pipeline_output["paths"]["script"],
            "chunks_path": pipeline_output["paths"]["chunks"],
            "script_preview": pipeline_output["script"]  
        }
        
        # Store metadata wrapper locally directly alongside script JSONs!
        save_json(job_id, "metadata.json", final_result)
        
        # Step 6: Trigger fully Completed into PSQL
        sync_update_job(job_id, JobStatus.completed, progress=100, result=final_result)
        
        logger.info(f"[PPT Task] Live generation fully completed Job {job_id}")
        return final_result

    except Exception as exc:
        logger.error(f"[PPT Task] Live AI generation failed: {exc}", exc_info=True)
        sync_update_job(job_id, JobStatus.failed, error=str(exc))
        # Exponential backoff retry natively executed by Celery Daemon
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
