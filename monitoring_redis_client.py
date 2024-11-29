import redis
import config
import time
from redis.exceptions import ConnectionError, TimeoutError
from retrying import retry

log_key = config.LOG_KEY
urls_created_metric_key = config.METRICS.URLS_CREATED_KEY
urls_redirected_metric_key = config.METRICS.URLS_REDIRECTED_KEY_PREFIX
retry_wait = config.REDIS_RETRY_WAIT
num_retries = config.REDIS_NUM_RETRIES

rds = redis.Redis(host=config.MONITORING_REDIS_HOST, port=config.MONITORING_REDIS_PORT, db=0)

@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def log(log_entry: str) -> None:
    try:
        timestamp = time.time()
        rds.zadd(log_key, {log_entry: timestamp})
    except (ConnectionError, TimeoutError) as e:
        print(f"Error logging entry {log_entry}: {e}")


@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def increment_url_created_count() -> None:
    try:
        response = rds.incr(urls_created_metric_key)
        print(f"URL count incremented: {response}")
    except (ConnectionError, TimeoutError) as e:
        print(f"Error incrementing URL count: {e}")

@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def increment_visit_count(short_url: str) -> None:
    try:
        rds.hincrby(urls_redirected_metric_key, short_url)
    except (ConnectionError, TimeoutError) as e:
        print(f"Error incrementing visit count for {short_url}: {e}")
        raise

@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def get_url_count() -> int:
    try:
        return int(rds.get(urls_created_metric_key) or 0)
    except (ConnectionError, TimeoutError) as e:
        print(f"Error getting URL count: {e}")
        raise

@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def get_visit_count(short_url: str) -> int:
    try:
        return int(rds.hget(urls_created_metric_key, short_url) or 0)
    except (ConnectionError, TimeoutError) as e:
        print(f"Error getting visit count for {short_url}: {e}")
        raise

if __name__ == "__main__":
    print(f"URL count: {get_url_count()}")
    try:
        pattern = f"{urls_redirected_metric_key}*"
        keys = rds.hgetall(urls_redirected_metric_key)
        print("Matched keys and their values:")
        for key in keys:
            print(f"{key.decode('utf-8')}: {int(keys[key])}")
        last_10_logs = rds.zrevrange(log_key, 0, 9, withscores=True)
        print(f"Last 10 log entries:")
        for log_entry, timestamp in last_10_logs:
            print(f"{log_entry.decode('utf-8')}")
    except (ConnectionError, TimeoutError) as e:
        print(f"Error getting top 10 visit counts: {e}")