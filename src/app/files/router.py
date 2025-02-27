from typing import Type
from fastapi import Depends, UploadFile, File as FileBody
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.engine import get_async_session
from src.fastkit.routers.base import BaseRouter
from src.app.files.models.file import File
from src.app.files.schemas.file import FileCreate, FileRead, FileUploadResponse
from src.app.files.service import FileService
from src.app.files.repository import FileRepository


class FileRouter(BaseRouter[File]):
    """Router for handling file operations."""

    def __init__(self, service_cls: Type[FileService], prefix: str):
        super().__init__(service_cls, FileUploadResponse, prefix)

        @self.router.post("/upload", response_model=FileUploadResponse)
        async def upload_file(
            file: UploadFile = FileBody(...),
            db_session: AsyncSession = Depends(get_async_session),
        ):
            """
            Upload a file and store it as Base64.
            """
            service = self.service_cls(db_session)
            return await service.upload(file)