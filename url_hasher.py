import secrets
import base64
from redis_client import try_set, get
from base_log import BASE_LOG
from typing import Tuple

log = BASE_LOG.getChild(__name__)
def generate_random_base64(length:int=6) -> str:
    random_bytes = secrets.token_bytes(length)
    base64_string = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode('utf-8')
    return base64_string

def create_short_url(long_url:str) -> Tuple[str, int] | None:
    short_url = generate_random_base64()
    collisions = 0
    try:
        while not try_set(short_url, long_url):
            collisions += 1
            short_url = generate_random_base64()
    except Exception as e:
        log.error(f"Error creating short URL for {long_url}: {e}")
        return None
    return short_url, collisions

def get_long_url(short_url:str) -> str|None:
    try:
        return get(short_url).decode('utf-8')
    except Exception as e:
        log.error(f"Error getting long URL for {short_url}: {e}")
        return None