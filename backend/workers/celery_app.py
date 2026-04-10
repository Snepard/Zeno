from celery import Celery
import os

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery(
    "ai_guruji_worker",
    broker=broker_url,
    backend=result_backend,
    include=[
        "workers.tasks.ppt_task",
        "workers.tasks.podcast_task"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True, # Safety logic: do not acknowledge task success until strictly finished
    worker_prefetch_multiplier=1 # Assign exact 1 task at a time to workers for better distribution
)
