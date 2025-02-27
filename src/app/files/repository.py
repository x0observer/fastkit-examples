from src.fastkit.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.files.models.file import File


class FileRepository(BaseRepository[File]):
    """
    Repository class for File entity.
    """

    def __init__(self, db_session: AsyncSession):
        super().__init__(File, db_session)
