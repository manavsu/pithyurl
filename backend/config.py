BASE_URL = "http://localhost:8000/"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

REDIS_RETRY_WAIT = 1000
REDIS_NUM_RETRIES = 2

# Monitoring
MONITORING_REDIS_HOST = "localhost"
MONITORING_REDIS_PORT = 16379

LOG_KEY = "logs"

class METRICS:
    URLS_CREATED_KEY = "num_urls_created"
    URLS_REDIRECTED_KEY_PREFIX = "visits:" # + short_url