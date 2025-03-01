import base64
from typing import List
from fastapi import UploadFile, HTTPException, Response
from src.middleware.engine import AsyncSession
from src.fastkit.services.base import BaseService
from .repository import FileRepository
from .schemas.file import FileUploadResponse
from .models.file import File


class FileService(BaseService[File]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        super().__init__(FileRepository(db_session))

    async def upload(self, file: UploadFile) -> FileUploadResponse:
        """
        Загружает один файл и сохраняет в БД.
        """
        file_data = await file.read()

        new_file = await self.repository.create_file(
            filename=file.filename,
            content_type=file.content_type,
            file_data=file_data
        )

        return FileUploadResponse(
            id=new_file.id,
            filename=new_file.filename,
            content_type=new_file.content_type
        )

    async def upload_multiple(self, files: List[UploadFile]) -> List[FileUploadResponse]:
        """
        Загружает несколько файлов через `FileRepository`.
        """
        file_dicts = []
        for file in files:
            file_data = await file.read()
            file_dicts.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "file_data": file_data
            })

        new_files = await self.repository.create_multiple_files(file_dicts)

        return [FileUploadResponse(
            id=file.id,
            filename=file.filename,
            content_type=file.content_type
        ) for file in new_files]
        
        
    async def get_decoded_file(self, file_id: int) -> Response:
        """Returns the file by ID, decoding the base64 back to binary format."""
        file = await self.repository.get_by_id(file_id)
        if not file or not file.base64_data:
            raise HTTPException(status_code=404, detail="File is not found")

        file_data = base64.b64decode(file.base64_data)

        return Response(content=file_data, media_type=file.content_type)