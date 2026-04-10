import os
import requests

from celery_app import celery_app
from db import mark_component_done, update_job

AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://localhost:8000")


@celery_app.task(bind=True, max_retries=3)
def generate_ppt_asset(self, payload: dict):
    job_id = payload["job_id"]
    try:
        resp = requests.post(
            f"{AI_ENGINE_URL}/pipelines/lecture/ppt",
            json={"job_id": job_id},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        update_job(job_id, "partial", {"ppt_url": data["ppt_url"]})
        mark_component_done(job_id, "ppt_done")
        return data
    except Exception as exc:
        raise self.retry(exc=exc)
