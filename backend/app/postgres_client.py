from sqlalchemy import create_engine, Column, String, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from retrying import retry
import config
from backend.app.base_log import BASE_LOG

log = BASE_LOG.getChild(__name__)

retry_wait = config.POSTGRES_RETRY_WAIT
num_retries = config.POSTGRES_NUM_RETRIES

DATABASE_URL = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class KeyValueStore(Base):
    __tablename__ = 'key_value_store'
    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def try_set(key: str, value: str) -> bool:
    session = SessionLocal()
    try:
        kv = KeyValueStore(key=key, value=value)
        session.add(kv)
        session.commit()
        return True
    except exc.IntegrityError:
        session.rollback()
        log.info(f"Key {key} already exists.")
        return False
    except (exc.OperationalError, exc.InterfaceError) as e:
        session.rollback()
        log.error(f"Error setting key {key}: {e}")
        raise
    finally:
        session.close()

@retry(stop_max_attempt_number=num_retries, wait_fixed=retry_wait)
def get(key: str) -> str | None:
    session = SessionLocal()
    try:
        kv = session.query(KeyValueStore).filter(KeyValueStore.key == key).first()
        return kv.value if kv else None
    except (exc.OperationalError, exc.InterfaceError) as e:
        log.error(f"Error getting key {key}: {e}")
        raise
    finally:
        session.close()