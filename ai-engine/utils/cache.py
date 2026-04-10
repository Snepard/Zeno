import json

import redis

from utils.settings import REDIS_URL

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def get_json(key: str):
    raw = redis_client.get(key)
    if not raw:
        return None
    return json.loads(raw)


def set_json(key: str, value, ttl_seconds: int = 3600):
    redis_client.setex(key, ttl_seconds, json.dumps(value))
