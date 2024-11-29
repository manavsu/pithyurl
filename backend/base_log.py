import logging
import logging.handlers
import monitoring_redis_client

class RedisHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        log_entry = self.format(record)
        monitoring_redis_client.log(log_entry)

BASE_LOG = logging.getLogger("pithy")
BASE_LOG.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
console_handler.setFormatter(console_formatter)
console_handler.setLevel(logging.INFO)

redis_handler = RedisHandler()
redis_formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(message)s')
redis_handler.setFormatter(redis_formatter)
redis_handler.setLevel(logging.DEBUG)

BASE_LOG.addHandler(console_handler)
BASE_LOG.addHandler(redis_handler)
BASE_LOG.propagate = False

logging.basicConfig(level=logging.INFO)

logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('traitlets').setLevel(logging.WARNING)

BASE_LOG.info("Base log initialized.")