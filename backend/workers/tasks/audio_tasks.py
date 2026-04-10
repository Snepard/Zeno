from workers.celery_app import celery_app
from ai_engine.tts.tts_manager import generate_audio_manager
from models.job import JobStatus, Job
from db.database import AsyncSessionLocal
from sqlalchemy.future import select
import asyncio
import logging

logger = logging.getLogger(__name__)

async def dynamically_save_audio_state(job_id: str, index_no: int, audio_path: str, total_units: int, is_podcast: bool = False):
    """
    Safely executes PostgreSQL updates directly within grouped concurrency bounds utilizing explicit 
    row-level FOR UPDATE locking logic natively mapping arrays back precisely.
    """
    async with AsyncSessionLocal() as session:
        # Secure concurrency locking bypassing overwritten race-conditions globally natively.
        qs = await session.execute(select(Job).where(Job.job_id == job_id).with_for_update())
        job = qs.scalar_one_or_none()
        if job:
            res = dict(job.result) if job.result else {}
            script = res.get("script", {})
            
            if is_podcast:
                items = script.get("dialogue", [])
                for idx, turn in enumerate(items):
                    if idx == index_no: 
                        turn["audio_url"] = f"/storage/{job_id}/podcast/turn_{index_no}.mp3"
            else:
                items = script.get("slides", [])
                for slide in items:
                    if slide["slide_no"] == index_no:
                        slide["audio_url"] = f"/storage/{job_id}/audio/slide_{index_no}.mp3"
                        
            # Incrementally jump 40% threshold split equally targeting 100% reliably 
            job.progress += int(40 / total_units)
            
            # Bound completion rules natively ensuring Frontend 100% strict matching
            if job.progress >= 99:
                job.progress = 100
                job.status = JobStatus.completed
            
            job.result = res
            session.add(job)
            await session.commit()
            logger.info(f"[Audio Progress Sync] Job {job_id} | Currently Progressing: {job.progress}%")


@celery_app.task(bind=True, max_retries=2)
def generate_ppt_audio_subtask(self, job_id: str, slide_no: int, text: str, total_slides: int):
    """Independent Subtask deployed parallel scaling explicitly per slide generating native outputs"""
    logger.info(f"Delegated Subtask processing presentation audio: Slide {slide_no} for Job {job_id}")
    try:
        audio_path = generate_audio_manager(text, job_id, f"slide_{slide_no}.mp3", subfolder="audio")
        asyncio.run(dynamically_save_audio_state(job_id, slide_no, audio_path, total_slides, is_podcast=False))
        return {"slide_no": slide_no, "audio_url": audio_path}
    except Exception as exc:
        logger.error(f"Slide Audio Fatal Generation Error: {exc}")
        raise self.retry(exc=exc, countdown=10)


@celery_app.task(bind=True, max_retries=2)
def generate_podcast_audio_subtask(self, job_id: str, turn_no: int, text: str, total_turns: int):
    """Independent Parallel Subtasks resolving audio chunks natively strictly per dialogue."""
    logger.info(f"Delegated Podcast Dialog audio generated exclusively natively: Turn {turn_no} | Job {job_id}")
    try:
        # Uses explicit podcast folder mappings maintaining structural MVP alignment natively.
        audio_path = generate_audio_manager(text, job_id, f"turn_{turn_no}.mp3", subfolder="podcast")
        asyncio.run(dynamically_save_audio_state(job_id, turn_no, audio_path, total_turns, is_podcast=True))
        return {"turn_no": turn_no, "audio_url": audio_path}
    except Exception as exc:
        logger.error(f"Podcast Thread Native Fallback Error Exception: {exc}")
        raise self.retry(exc=exc, countdown=10)
