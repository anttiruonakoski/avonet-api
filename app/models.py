from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Bird(Base):
    __tablename__ = "bird_taxons"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

