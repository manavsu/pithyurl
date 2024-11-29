import redis
import config
from redis.exceptions import ConnectionError, TimeoutError
from retrying import retry
from base_log import BASE_LOG

log = BASE_LOG.getChild(__name__)

retry_wait = config.REDIS_RETRY_WAIT
num_retries = config.REDIS_NUM_RETRIES

rds = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def try_set(key: str, value: str) -> bool:
    try:
        return rds.set(key, value, nx=True) == True
    except (ConnectionError, TimeoutError) as e:
        log.error(f"Error setting key {key}: {e}")
        raise

@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def get(key: str) -> str | None:
    try:
        return rds.get(key)
    except (ConnectionError, TimeoutError) as e:
        log.error(f"Error getting key {key}: {e}")
        raise