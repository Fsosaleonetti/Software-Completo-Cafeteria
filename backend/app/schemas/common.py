from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class ORMModel(BaseModel):
    class Config:
        from_attributes = True


class Paginated(Generic[T], GenericModel):
    items: List[T]
    total: int
    page: int
    size: int


class AuditInfo(BaseModel):
    created_at: datetime
    updated_at: datetime


class StatusMessage(BaseModel):
    detail: str
    meta: Optional[dict] = None
