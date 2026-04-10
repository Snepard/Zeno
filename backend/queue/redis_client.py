import redis.asyncio as redis
import os
import json
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

async def push_to_queue(queue_name: str, payload: dict):
    """
    Pushes a job payload directly to a Redis queue.
    """
    try:
        data = json.dumps(payload)
        await redis_client.rpush(queue_name, data)
        logger.info(f"Pushed raw payload {payload.get('job_id')} to strict redis queue {queue_name}")
    except Exception as e:
        logger.error(f"Failed to push strictly to Redis queue: {e}")
        raise e

async def get_redis():
    """Dependency to get Redis native async client if needed inside FastAPI endpoints"""
    return redis_client
