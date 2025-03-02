import base64
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.fastkit.repositories.base import BaseRepository
from src.app.files.models.file import File




class FileRepository(BaseRepository[File]):
    """
    Repository class for File entity.
    """

    def __init__(self, db_session: AsyncSession):
        super().__init__(File, db_session)


    async def create_file(self, filename: str, content_type: str, file_data: bytes) -> File:
        """Создаёт и сохраняет файл в БД (Base64-кодирование)."""
        base64_data = base64.b64encode(file_data).decode("utf-8")

        new_file = File(
            filename=filename,
            content_type=content_type,
            base64_data=base64_data
        )

        async with self.uow.transaction():  # Unit of Work управляет транзакцией
            self.uow.db.add(new_file)
            await self.uow.db.flush()
            await self.uow.db.refresh(new_file)

        return new_file
    
    async def create_multiple_files(self, files: List[dict]) -> List[File]:
        """
        Создаёт несколько файлов за одну транзакцию.
        :param files: Список словарей с данными файлов.
        """
        new_files = [
            File(
                filename=file["filename"],
                content_type=file["content_type"],
                base64_data=base64.b64encode(file["file_data"]).decode("utf-8")
            ) for file in files
        ]

        async with self.uow.transaction():  
            self.uow.db.add_all(new_files)
            await self.uow.db.flush()
            for file in new_files:
                await self.uow.db.refresh(file)

        return new_files