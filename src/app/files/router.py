from typing import Type
from fastapi import Depends, UploadFile, File as FileBody, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.engine import get_async_session
from src.fastkit.routers.base import BaseRouter
from src.app.files.models.file import File
from src.app.files.schemas.file import FileCreate, FileRead, FileUploadResponse, ALLOWED_CONTENT_TYPES
from src.app.files.service import FileService


class FileRouter(BaseRouter[File, FileCreate, FileRead]):
    """Router for handling file operations."""

    def __init__(self, service_cls: Type[FileService], prefix: str):
        super().__init__(service_cls, prefix, FileCreate, FileRead)

        @self.router.post("/upload", response_model=FileUploadResponse)
        async def upload_file(
            file: UploadFile = FileBody(...),
            db_session: AsyncSession = Depends(get_async_session),
        ) -> FileUploadResponse:
            """
            Upload a file and store it.
            """
            
            if file.content_type not in ALLOWED_CONTENT_TYPES:
                raise HTTPException(status_code=400, detail=f"Unsupported content type: {file.content_type}")
            
            service = self.service_cls(db_session)
            return await service.upload(file)
        
        @self.router.get("/{file_id}/decoded")
        async def get_decoded_file(
            file_id: int,
            db_session: AsyncSession = Depends(get_async_session),
        ) -> Response:
            """
            Retrieve a decoded file by ID.
            """
            service = self.service_cls(db_session)
            return await service.get_decoded_file(file_id)
