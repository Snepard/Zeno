"""
Thread-based background runner — replaces Celery + Redis entirely.
Jobs are dispatched to a Python daemon thread immediately on API call.
"""
import threading
import logging

from db.job_store import update_job
from ai_engine.pipelines.ppt_pipeline import run_ppt_pipeline
from ai_engine.pipelines.podcast_pipeline import run_podcast_pipeline
from ai_engine.tts.tts_manager import generate_audio_manager

logger = logging.getLogger(__name__)


def _run_ppt(job_id: str, topic: str):
    try:
        update_job(job_id, status="processing", progress=10)
        pipeline_output = run_ppt_pipeline(job_id, topic)
        update_job(job_id, status="processing", progress=60,
                   result={"topic": topic, "script": pipeline_output["script"]})

        # Generate audio per slide sequentially (no Celery group needed)
        slides = pipeline_output["script"].get("slides", [])
        total = len(slides)
        for i, slide in enumerate(slides):
            try:
                text = slide.get("explanation") or slide.get("content", "")
                audio_path = generate_audio_manager(job_id, slide["slide_no"], text)
                slide["audio_url"] = f"/storage/{job_id}/audio/slide_{slide['slide_no']}.mp3"
            except Exception as ae:
                logger.warning(f"Audio failed for slide {slide.get('slide_no')}: {ae}")
            progress = 60 + int(((i + 1) / total) * 40)
            update_job(job_id, progress=progress)

        # Write final result with updated audio_urls
        update_job(job_id, status="completed", progress=100,
                   result={"script": pipeline_output["script"]})
        logger.info(f"PPT job {job_id} completed.")

    except Exception as e:
        logger.error(f"PPT job {job_id} failed: {e}", exc_info=True)
        update_job(job_id, status="failed", error=str(e))


def _run_podcast(job_id: str, topic: str):
    try:
        update_job(job_id, status="processing", progress=10)
        pipeline_output = run_podcast_pipeline(job_id, topic)
        update_job(job_id, status="processing", progress=60,
                   result={"topic": topic, "script": pipeline_output["script"]})

        dialogue = pipeline_output["script"].get("dialogue", [])
        total = len(dialogue)
        for i, turn in enumerate(dialogue):
            try:
                text = turn.get("text", "")
                generate_audio_manager(job_id, i + 1, text)
                turn["audio_url"] = f"/storage/{job_id}/audio/slide_{i + 1}.mp3"
            except Exception as ae:
                logger.warning(f"Audio failed for turn {i+1}: {ae}")
            progress = 60 + int(((i + 1) / total) * 40)
            update_job(job_id, progress=progress)

        update_job(job_id, status="completed", progress=100,
                   result={"script": pipeline_output["script"]})
        logger.info(f"Podcast job {job_id} completed.")

    except Exception as e:
        logger.error(f"Podcast job {job_id} failed: {e}", exc_info=True)
        update_job(job_id, status="failed", error=str(e))


def dispatch_job(job_id: str, job_type: str, topic: str):
    """Fire-and-forget: spawn a daemon thread for the job."""
    target = _run_ppt if job_type == "ppt" else _run_podcast
    t = threading.Thread(target=target, args=(job_id, topic), daemon=True)
    t.start()
    logger.info(f"Dispatched {job_type} job {job_id} to background thread.")
