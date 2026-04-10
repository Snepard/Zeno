import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "zeno_workers",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["lecture_worker", "podcast_worker", "ppt_worker"],
)

celery_app.conf.task_routes = {
    "lecture_worker.*": {"queue": "lecture"},
    "podcast_worker.*": {"queue": "podcast"},
    "ppt_worker.*": {"queue": "ppt"},
}

celery_app.conf.task_default_retry_delay = 5
celery_app.conf.task_acks_late = True
celery_app.conf.worker_prefetch_multiplier = 1
