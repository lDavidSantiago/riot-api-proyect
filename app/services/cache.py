import json
import redis
from app.core.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

async def get_or_set(key: str, ttl: int, fetch_fn):
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    data = await fetch_fn()
    r.setex(key, ttl, json.dumps(data))
    return data
