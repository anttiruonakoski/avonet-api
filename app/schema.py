from pydantic import BaseModel


class TaxonBase(BaseModel):
    title: str
    description: str | None = None


class Bird(ItemBase):
    id: int

    class Config:
        orm_mode = True