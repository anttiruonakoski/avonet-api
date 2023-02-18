from pydantic import BaseModel, create_model
from .database import get_db_column_typing_as_python_types
from typing import List
from .database import create_database

# we need to create database before schema, because dynamic schemas depend on database model
column_types = create_database()

class TaxonBase(BaseModel):
    # let's keep Base class for now
    pass


class PydanticBird(TaxonBase):
    id: int
    species: str | None = None


class Config:
    orm_mode = True


def get_bird_schema() -> BaseModel:
    # table = Table(table_name, metadata, autoload_with=engine)
    # column_types = {(c.name, c.type.python_type) for c in table.columns}

    # This API in read-only and would not need model for validation etc.
    # However, constant property order in JSON responses is nice to have and
    # that's why we create Pydantic models on-the-fly to correspond database field order
    # column_typing = dict(id=(int, None), species=(str | None, None))

    # Let's be lazy and get column types and order from DB table. Original data source field ordering will remain.

    column_typing = get_db_column_typing_as_python_types()
    # print(column_typing)

    return create_model("Bird", **column_typing, __config__=Config)


BirdBase = get_bird_schema()


class BirdAll(BaseModel):
    bird: List | None
    class Config:
        orm_mode = True
