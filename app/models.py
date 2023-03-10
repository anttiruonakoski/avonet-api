from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    DateTime,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy_future import paginate


from .database import table_name, metadata, engine
from sqlalchemy.ext.automap import automap_base


def ReflectedModel(classname):
    metadata.reflect(engine)

    # ... or just define our own Table objects with it (or combine both)
    Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        extend_existing=True,
    )

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)
    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare()

    return getattr(Base.classes, classname)
