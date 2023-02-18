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

from .database import table_name, metadata, engine
from sqlalchemy.ext.automap import automap_base

def get_column(dtype: str) -> Column:
    """Very crude Pandas dtype string alias to SqlAlchemy CamelCase datatype mapping
    Args:
        dtype (str): Pandas dtype.astype(str)
    Returns:
        Column: SqlAlchemy ORM class
    """

    if "bool" in dtype:
        cc_type = Boolean
    elif "int" in dtype:
        cc_type = Integer
    elif "float" in dtype:
        cc_type = Numeric
    elif "datetime" in dtype:
        cc_type = DateTime
    else:
        cc_type = String
    return Column(cc_type)


def ReflectedBird():
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

    return Base.classes.bird