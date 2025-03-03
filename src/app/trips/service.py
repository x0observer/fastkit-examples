


from typing import List, Optional
from fastapi import UploadFile
from src.middleware.engine import AsyncSession
from src.fastkit.services.base import BaseService
from src.fastkit.utils.serverless import serverless, serviceable, Provide
from src.app.files.service import FileService
from .repository import TripRepository, TripImageRepository
from .models.trip import Trip, TripImage
from .schemas.trip import TripCreate, TripResponse

@serverless([FileService])
class TripService(BaseService[Trip]):
    """Сервис для работы с поездками, поддерживающий загрузку изображений."""

    def __init__(self, db_session: AsyncSession, ):
        super().__init__(TripRepository(db_session))
        self.trip_image_repository = TripImageRepository(db_session)
        self.db_session = db_session

    @serviceable
    async def create_with_images(
        self,
        trip_data: TripCreate,
        images: Optional[List[UploadFile]] = None,
        file_service: FileService = Provide(FileService)
    ) -> TripResponse:
        """Создаёт поездку и загружает изображения через FileService."""
        
        async with self.repository.uow.transaction():
            trip = await self.create(trip_data)

            image_urls = []
            if images:
                print(f"🔍 FileRepository -> db_session type: {type(self.db_session)}")
                image_urls = await self._upload_images_via_service(file_service, images)

            # Сохраняем ссылки на изображения
            await self.trip_image_repository.create_many(
                [TripImage(trip_id=trip.id, image_url=url) for url in image_urls]
            )

            return TripResponse(
                id=trip.id,
                title=trip.title,
                images=image_urls
            )

    async def _upload_images_via_service(
        self, file_service: FileService, images: List[UploadFile]
    ) -> List[str]:
        """Загружает файлы через FileService и возвращает ссылки."""
        
        image_urls = []
        for image in images:
            uploaded_file = await file_service.upload(image)
            image_urls.append(f"http://0.0.0.0:8000/files/{uploaded_file.id}/decoded")

        return image_urls