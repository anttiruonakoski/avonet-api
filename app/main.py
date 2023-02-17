import logging
import os
from typing import Union

from fastapi import FastAPI, Request
from .database import SessionLocal, engine

# browser side requests need ROOT_PATH to work on reverse_proxy, to correspond with server location
app = FastAPI(root_path=os.environ.get('ROOT_PATH'))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[logging.FileHandler("avonet-api.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request):
    return {"Hello": "World", "root_path": request.scope.get("root_path")}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}