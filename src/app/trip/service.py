
from src.middleware.engine import AsyncSession
from src.fastkit.services.base import BaseService
from .repository import TripRepository
from .models.trip import Trip   


class TripService(BaseService[Trip]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        super().__init__(TripRepository(db_session))


