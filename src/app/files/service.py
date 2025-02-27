import base64
from fastapi import UploadFile
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
        Uploads a file, encodes it in Base64, and stores it in the database.
        Uses `with db_session.begin()` to ensure transaction safety.
        """
        file_data = await file.read()
        base64_data = base64.b64encode(file_data).decode("utf-8")

        new_file = File(
            filename=file.filename,
            content_type=file.content_type,
            base64_data=base64_data
        )

        async with self.db_session.begin():
            self.db_session.add(new_file)
            await self.db_session.flush()  
            await self.db_session.refresh(new_file)

        return FileUploadResponse(
            id=new_file.id,
            filename=new_file.filename,
            content_type=new_file.content_type,
            # base64_data=new_file.base64_data,
        )
