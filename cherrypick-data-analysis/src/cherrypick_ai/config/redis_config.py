import redis
from src.cherrypick_ai.config.env_config import REDIS_URL, REDIS_PORT

def get_redis_client():
    return redis.StrictRedis(host=REDIS_URL, port=REDIS_PORT, db=0, decode_responses=True)