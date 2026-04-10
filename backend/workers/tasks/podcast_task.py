from workers.celery_app import celery_app
from workers.tasks.utils import sync_update_job
from storage.local_storage import save_json
from models.job import JobStatus
from ai_engine.pipelines.podcast_pipeline import run_podcast_pipeline
from workers.tasks.audio_tasks import generate_podcast_audio_subtask
from celery import group
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def generate_podcast_task(self, job_id: str, user_id: str, topic: str):
    logger.info(f"[Main Podcast Runner] Process successfully hooked natively: Job {job_id} on '{topic}'")
    
    try:
        sync_update_job(job_id, JobStatus.processing, progress=10)
        sync_update_job(job_id, JobStatus.processing, progress=40)
        
        pipeline_output = run_podcast_pipeline(job_id, topic)
        
        initial_result = {
            "topic": topic,
            "script_path": pipeline_output["paths"]["script"],
            "chunks_path": pipeline_output["paths"]["chunks"],
            "script": pipeline_output["script"],
        }
        
        # Stage 2 Audio Sub-processing Initializer (60%)
        sync_update_job(job_id, JobStatus.processing, progress=60, result=initial_result)
        
        dialogues = pipeline_output["script"].get("dialogue", [])
        total_turns = len(dialogues)
        
        if total_turns > 0:
            logger.info(f"Unleashing {total_turns} distinct Podcast voice strings optimally natively...")
            subtasks = [
                generate_podcast_audio_subtask.s(job_id, idx, turn["text"], total_turns)
                for idx, turn in enumerate(dialogues)
            ]
            # Fire Async Multi-threads strictly avoiding blocking architecture rules.
            group(subtasks).apply_async()
        else:
            sync_update_job(job_id, JobStatus.completed, progress=100)

        return True

    except Exception as exc:
        logger.error(f"[Main Podcast Flow] Critical failure internally processing LLMs natively: {exc}", exc_info=True)
        sync_update_job(job_id, JobStatus.failed, error=str(exc))
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
