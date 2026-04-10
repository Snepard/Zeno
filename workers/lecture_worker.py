import os
from celery import chord
import requests

from celery_app import celery_app
from db import mark_component_done, update_job

AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://localhost:8000")


@celery_app.task(bind=True, max_retries=3)
def process_lecture_job(self, payload: dict):
    job_id = payload["job_id"]
    try:
        slides_resp = requests.post(
            f"{AI_ENGINE_URL}/pipelines/lecture/slides",
            json={"pdf_url": payload["pdf_url"], "title": payload.get("title", "Lecture")},
            timeout=60,
        )
        slides_resp.raise_for_status()
        slides_data = slides_resp.json()

        update_job(job_id, "partial", {"slides": slides_data["slides"]})

        tts_jobs = []
        for slide in slides_data["slides"]:
            tts_jobs.append(
                generate_slide_audio.s(
                    {
                        "job_id": job_id,
                        "slide_number": slide["slide_number"],
                        "text": slide["speaker_notes"],
                    }
                )
            )

        # TTS fan-out runs in parallel and completes as one component.
        chord(tts_jobs)(finalize_lecture_audio.s(job_id))
        celery_app.send_task("ppt_worker.generate_ppt_asset", args=[{"job_id": job_id}])

        return {"job_id": job_id, "status": "partial"}
    except Exception as exc:
        update_job(job_id, "failed", error=str(exc))
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3)
def generate_slide_audio(self, payload: dict):
    try:
        resp = requests.post(
            f"{AI_ENGINE_URL}/pipelines/lecture/slide-audio",
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        update_job(
            payload["job_id"],
            "partial",
            {f"audio_slide_{payload['slide_number']}": data["audio_url"]},
        )
        return data
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task
def finalize_lecture_audio(_results, job_id: str):
    mark_component_done(job_id, "audio_done")
    return {"job_id": job_id, "audio": "done"}
