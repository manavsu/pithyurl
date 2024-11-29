from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import URL
from typing import Tuple

from app.base_log import BASE_LOG
from app.url_hasher import generate_random_base64

log = BASE_LOG.getChild(__name__)

def get_long_url(short_url:str, db:Session) -> str|None:
    url = db.query(URL).filter(URL.short_url == short_url).first()
    if url:
        url.clicks += 1
        db.commit()
        return url.url
    return None

def create_short_url(long_url:str, db:Session) -> Tuple[str, int] | None:
    short_url = generate_random_base64()
    collisions = 0
    while True:
        try:
            new_url = URL(short_url=short_url, url=long_url)
            db.add(new_url)
            db.commit()
            return short_url, collisions
        except IntegrityError:
            db.rollback()
            collisions += 1
            short_url = generate_random_base64()
        except Exception as e:
            log.error(f"Error creating short URL for {long_url}: {e}")
            return None
        

if __name__ == "__main__":
    from app.models import DB_Session_Maker
    from app.models import URL, LogEntry 
    db = DB_Session_Maker()
    for url in db.query(URL).all():
        print(url)
    for log in db.query(LogEntry).all():
        print(log)