import logging
import os, sys

import pandas as pd

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from .config import DB_FILE, DATA_DIR, DATA_FILE

SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()
metadata = MetaData()

csv_file = DATA_DIR / DATA_FILE
table_name = "bird"

logger = logging.getLogger(__name__)


def get_dataframe() -> pd.DataFrame:
    logger.info(f"Reading {csv_file}.")

    df = pd.read_csv(
        csv_file,
        sep=",",
        true_values=["YES"],
        false_values=["NO"],
    )
    COLUMNS = [str.lower(c).rstrip("1").replace(".", "_") for c in df.columns]
    df.columns = COLUMNS
    # Add id column for foreign key
    # df = df.rename_axis('ID').reset_index()
    print(df.head())
    logger.info(f"{csv_file} was parsed. OK!")
    return df


def create_database():
    """
    Function that creates a new SQLite database from the CSV
    data file. This file implicitly uses the file referenced
    in the DB_FILE constant

    :return: None
    """
    logger.info(f"Importing Avonet data to{DB_FILE}")

    if os.path.exists(DB_FILE):
        # Remove any old DB files, as this allows us to
        # start the API up with a new projections file.
        # The API itself is read-only, thus this is fine.
        os.remove(DB_FILE)

    df = get_dataframe()

    try:
        # we add index as a sql column. index is ascending sequence of unique ints and is safe candidate key.
        # on model side, we define Table object id column as PK
        # unfortunately there is no parameter to define constraints in to_sql()
        # this practise is not a problem, because we are not doing any inserts or updates
        with engine.begin() as connection:
            df.to_sql(
                table_name,
                con=connection,
                index=True,
                index_label="id",
                if_exists="replace",
            )
    except SQLAlchemyError as e:
        logger.error("The database creation failed!", e)
        raise
    else:
        logger.info("The database was created. OK!")

    return None


def get_columns(df: pd.DataFrame) -> dict:
    return df.dtypes.astype(str).to_dict()


def get_db_column_typing_as_python_types():
    table = Table(table_name, metadata, autoload_with=engine)
    columns = {str(c.name): (c.type.python_type, None) for c in table.columns}
    return columns


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
