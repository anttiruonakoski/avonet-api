import logging

from sqlalchemy.orm import Session
from .models import ReflectedModel

# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def get_bird(db: Session, bird_id: int):
    Bird = ReflectedModel('bird')
    logger.debug(f"Retrieving data for bird {bird_id}.")
    return db.query(Bird).filter(Bird.id == bird_id).first()


def get_all_birds(db: Session, limit):
    Bird = ReflectedModel('bird')
    logger.debug(f"Retrieving all birds.")
    return db.query(Bird).limit(limit).all()
