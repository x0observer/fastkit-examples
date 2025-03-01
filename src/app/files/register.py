
from src.app.files.service import FileService
from src.app.files.router import FileRouter
from src.middleware.engine import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# ...

def get_file_service(db_session: AsyncSession = Depends(get_async_session)) -> FileService:
    """Возвращает экземпляр FileService с уже подключенной сессией."""
    return FileService(db_session)

file_router = FileRouter(service_cls=FileService, prefix="/files").get_router()