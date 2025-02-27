from typing import Type
from src.fastkit.routers.base import BaseRouter

from src.app.trip.models.trip import Trip
from src.app.trip.schemas.trip import TripCreate, TripRead
from src.app.trip.service import TripService


class TripRouter(BaseRouter[Trip, TripCreate, TripRead]):
    """Router for handling file operations."""

    def __init__(self, service_cls: Type[TripService], prefix: str):
        super().__init__(service_cls, prefix, TripCreate, TripRead)

 