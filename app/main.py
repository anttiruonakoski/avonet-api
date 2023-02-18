import logging
import os
from typing import Union, List
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from fastapi import FastAPI, Request, Depends, HTTPException
from .database import SessionLocal, engine, create_database, get_db
from .schema import BirdBase, BirdAll, get_bird_schema

# from .models import ReflectedBird
from app import api_read

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[logging.FileHandler("avonet-api.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# print(list(inspect(bird).columns))

# browser side requests need ROOT_PATH to work on reverse_proxy, to correspond with server location
app = FastAPI(root_path=os.environ.get("ROOT_PATH"))


@app.get("/bird/{bird_id}", response_model=BirdBase)
def get_bird(bird_id: int, db: Session = Depends(get_db)):
    logger.info(f"Retrieving bird by id {bird_id}.")
    bird = api_read.get_bird(db, bird_id=bird_id)

    if bird is None:
        logger.warning(f"bird not found by id {bird_id}.")
        raise HTTPException(status_code=404, detail="bird not found.")

    logger.info(f"Successfully retrieved bird by id {bird_id}.")
    return bird


@app.get("/bird/", response_model=List[BirdBase])
def get_all_birds(limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Retrieving all birds")
    birds = api_read.get_all_birds(db, limit=limit)

    if birds is None:
        logger.warning(f"birds not found")
        raise HTTPException(status_code=404, detail="birds not found.")

    logger.info(f"Successfully retrieved all birds")
    return birds


@app.get("/")
def read_root(request: Request):
    return {"Hello": "World", "root_path": request.scope.get("root_path")}

