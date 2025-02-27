from src.fastkit.repositories.base import BaseRepository
from src.app.trip.models.trip  import Trip
from sqlalchemy.ext.asyncio import AsyncSession



class TripRepository(BaseRepository[Trip]):
    """
    Repository class for Trip entity.
    """

    def __init__(self, db_session: AsyncSession):
        super().__init__(Trip, db_session)
