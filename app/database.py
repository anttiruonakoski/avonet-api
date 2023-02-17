import logging
import os

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DB_FILE, DATA_DIR, DATA_FILE

SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

csv_file = DATA_DIR + DATA_FILE

logger = logging.getLogger(__name__)

DB_COLUMNS = [
]

def get_dataframe() -> pd.DataFrame:
    logger.debug(f"Luetaan {csv_file}.")

    df = pd.read_csv(csv_file)

    # Rename the Underdog CSV column headers with our table column names
    df.columns = DB_COLUMNS

    logger.debug("Successfully parsed Underdog CSV.")
    return df