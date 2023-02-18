from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base, get_columns

columns = get_columns()


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


class Bird(Base):
    __tablename__ = "bird_taxons"
    _table_args__ = {"extend_existing": True}


for variable, datatype in columns.items():
    setattr(Bird, variable, get_column(datatype))
