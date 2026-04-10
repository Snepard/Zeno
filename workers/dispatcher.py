import json
import os
import time

import redis
from dotenv import load_dotenv

from celery_app import celery_app

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_MAP = {
    "jobs:lecture": "lecture_worker.process_lecture_job",
    "jobs:podcast": "podcast_worker.process_podcast_job",
    "jobs:flashcards": "podcast_worker.process_flashcards_job",
}


def run_dispatcher() -> None:
    while True:
        item = redis_client.brpop(list(QUEUE_MAP.keys()), timeout=3)
        if not item:
            continue

        queue_name, raw = item
        task_name = QUEUE_MAP[queue_name]

        payload = json.loads(raw)
        celery_app.send_task(task_name, args=[payload])


if __name__ == "__main__":
    run_dispatcher()
