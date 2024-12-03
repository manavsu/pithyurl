from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from config import BASE_URL
from app.base_log import BASE_LOG
from app.models import DB_Session_Maker
from app.url_operations import create_short_url, get_long_url

log = BASE_LOG.getChild(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = DB_Session_Maker()
    try:
        yield db
    finally:
        db.close()

class URL(BaseModel):
    url: str

@app.post("/urls")
def create_url(url: URL, db:Session=Depends(get_db)):
    result = create_short_url(url.url, db)
    if result is None:
        log.info(f"Failed to create short URL for {url.url}.")
        raise HTTPException(status_code=500, detail="Internal server error.")
    hash, collisions = result
    short_url = BASE_URL + hash
    log.info(f"{url.url} -> {hash} created with {collisions} collisions.")
    return URL(url=short_url)

@app.get("/{short_url}")
def read_item(short_url: str, db: Session=Depends(get_db)):
    long_url = get_long_url(short_url, db)
    if long_url is None:
        log.info(f"{short_url} not found.")
        raise HTTPException(status_code=404, detail="Not found.")
    
    log.info(f"{short_url} -> {long_url} redirected.")
    return RedirectResponse(url=long_url, status_code=302)

app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="static")
