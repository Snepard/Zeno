import redis.asyncio as redis
import json
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

async def push_to_queue(queue_name: str, payload: dict):
    """
    Pushes a job payload to a specified Redis list (queue).
    Placeholder for actual worker integration.
    """
    try:
        data = json.dumps(payload)
        await redis_client.rpush(queue_name, data)
        logger.info(f"Pushed job {payload.get('job_id')} to queue {queue_name}")
    except Exception as e:
        logger.error(f"Failed to push to Redis queue: {e}")
        raise e

async def get_redis():
    """Dependency to get Redis client"""
    return redis_client
