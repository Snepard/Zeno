import os
from celery import chord
import requests

from celery_app import celery_app
from db import mark_component_done, update_job

AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://localhost:8000")


@celery_app.task(bind=True, max_retries=3)
def process_podcast_job(self, payload: dict):
    job_id = payload["job_id"]
    try:
        dialogue_resp = requests.post(
            f"{AI_ENGINE_URL}/pipelines/podcast/dialogue",
            json={"pdf_url": payload["pdf_url"]},
            timeout=60,
        )
        dialogue_resp.raise_for_status()
        dialogue_data = dialogue_resp.json()

        update_job(job_id, "partial", {"dialogue": dialogue_data["dialogue"]})

        turn_jobs = []
        for turn in dialogue_data["dialogue"]:
            turn_jobs.append(generate_turn_audio.s({"job_id": job_id, **turn}))

        chord(turn_jobs)(finalize_podcast_audio.s(job_id))
        return {"job_id": job_id, "status": "partial"}
    except Exception as exc:
        update_job(job_id, "failed", error=str(exc))
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3)
def generate_turn_audio(self, payload: dict):
    try:
        resp = requests.post(
            f"{AI_ENGINE_URL}/pipelines/podcast/turn-audio",
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        update_job(
            payload["job_id"],
            "partial",
            {f"audio_turn_{payload['turn']}": data["audio_url"]},
        )
        return data
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3)
def process_flashcards_job(self, payload: dict):
    job_id = payload["job_id"]
    try:
        resp = requests.post(
            f"{AI_ENGINE_URL}/pipelines/rag/flashcards",
            json={"pdf_url": payload["pdf_url"], "count": payload.get("count", 20)},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        update_job(job_id, "complete", {"flashcards": data["cards"]})
        return data
    except Exception as exc:
        update_job(job_id, "failed", error=str(exc))
        raise self.retry(exc=exc)


@celery_app.task
def finalize_podcast_audio(_results, job_id: str):
    mark_component_done(job_id, "audio_done")
    return {"job_id": job_id, "audio": "done"}
