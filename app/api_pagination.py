from typing import TypeVar, Generic

from fastapi import Query

from fastapi_pagination.default import Page as BasePage, Params as BaseParams

T = TypeVar("T")


class Params(BaseParams):
    size: int = Query(100, ge=10, le=1000, description="Page size")


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params
