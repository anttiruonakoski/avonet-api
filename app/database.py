import logging
import os

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DB_FILE, DATA_DIR, DATA_FILE

SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

csv_file = DATA_DIR / DATA_FILE

logger = logging.getLogger(__name__)


def get_dataframe() -> pd.DataFrame:
    logger.debug(f"Luetaan {csv_file}.")

    df = pd.read_csv(
        csv_file,
        sep=",",
        true_values=["YES"],
        false_values=["NO"],
    )
    COLUMNS = [str.lower(c).rstrip("1").replace(".", "_") for c in df.columns]
    # Rename the Underdog CSV column headers with our table column names
    df.columns = COLUMNS

    logger.debug(f"Luettu {csv_file}.")
    return df


def create_database():
    """
    Function that creates a new SQLite database from the CSV
    data file. This file implicitly uses the file referenced
    in the UNDERDOG_CSV constant

    :return: None
    """
    logger.info("Tuodaan AVONET data tietokantaan.")

    if os.path.exists(DB_FILE):
        # Remove any old DB files, as this allows us to
        # start the API up with a new projections file.
        # The API itself is read-only, thus this is fine.
        os.remove(DB_FILE)

    Base.metadata.create_all(bind=engine)
    df = get_dataframe()

    try:
        with engine.begin() as connection:
            df.to_sql("bird_taxons", con=connection, index=False, if_exists="append")
    except SQLAlchemyError as e:
        logger.error("The database creation failed!", e)
        raise
    else:
        logger.info("Tietokanta luotiin.")


def get_colums(df: pd.DataFrame) -> dict:
    df.dtypes.astype(str).to_dict()
