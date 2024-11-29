import redis
import config
import time

log_key = config.LOG_KEY

rds = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

def try_set(key:str, value:str) -> bool:
    return rds.set(key, value, nx=True) == True

def get(key:str) -> str|None:
    return rds.get(key)

def log(log_entry:str) -> None:
    timestamp = time.time()
    rds.zadd(log_key, {log_entry: timestamp})