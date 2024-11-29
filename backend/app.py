from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from url_hasher import create_short_url, get_long_url
from fastapi.responses import RedirectResponse
from config import BASE_URL
from base_log import BASE_LOG
from monitoring_redis_client import increment_url_created_count, increment_visit_count

log = BASE_LOG.getChild(__name__)

class URL(BaseModel):
    url: str


app = FastAPI()

@app.get("/")
def read_root():
    return "I'm alive!"

@app.post("/urls")
def create_url(url: URL):
    result = create_short_url(url.url)
    if result is None:
        log.info(f"Failed to create short URL for {url.url}.")
        raise HTTPException(status_code=500, detail="Internal server error.")
    hash, collisions = result
    short_url = BASE_URL + hash
    increment_url_created_count()
    log.info(f"{url.url} -> {hash} created with {collisions} collisions.")
    return URL(url=short_url)

@app.get("/{short_url}")
def read_item(short_url: str):
    long_url = get_long_url(short_url)
    if long_url is None:
        log.info(f"{short_url} not found.")
        raise HTTPException(status_code=404, detail="Not found.")
    increment_visit_count(short_url)
    log.info(f"{short_url} -> {long_url} redirected.")
    return RedirectResponse(url=long_url, status_code=302)

