import redis
from .env import REDIS_URL, REDIS_PORT

def get_redis_client():
    return redis.StrictRedis(host=REDIS_URL, port=REDIS_PORT, db=0, decode_responses=True)

def get_redis_client_not_decode():
    return redis.StrictRedis(host=REDIS_URL, port=REDIS_PORT, db=0, decode_responses=False)