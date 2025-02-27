from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.engine import get_async_session
from src.fastkit.routers.base import BaseRouter
from src.app.files.schemas.file import FileCreate, FileRead
from src.app.files.service import FileService
from src.app.files.repository import FileRepository
from src.app.files.router import FileRouter
# ...
file_router = FileRouter(
    service_cls=FileService,  # ...
    schema=FileCreate,
    prefix="/files"
).get_router()