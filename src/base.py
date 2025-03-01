from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Readable(BaseModel):
    """
    Base schema for read operations, containing common attributes.
    """
    id: Optional[int]
    created_at: Optional[datetime]


class Paginatable(BaseModel):
    """
    Base schema for pagination operations, containing common attributes.
    """
    page: Optional[int] = 1
    items_per_page: Optional[int] = 10
