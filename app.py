from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from url_hasher import create_short_url, get_long_url
from fastapi.responses import RedirectResponse

from base_log import BASE_LOG

log = BASE_LOG.getChild(__name__)

class URL(BaseModel):
    url: str


app = FastAPI()

@app.get("/")
def read_root():
    return "I'm alive!"

@app.post("/urls")
def create_url(url: URL):
    short_url, collisions = create_short_url(url.url)
    log.info(f"{url.url} -> {short_url} created with {collisions} collisions.")
    return URL(url=short_url)

@app.get("/{short_url}")
def read_item(short_url: str):
    long_url = get_long_url(short_url)
    if long_url is None:
        log.info(f"{short_url} not found.")
        raise HTTPException(status_code=404, detail="Not found.")
    log.info(f"{short_url} -> {long_url} redirected.")
    return RedirectResponse(url=long_url, status_code=302)

