

from fastapi import Depends, Request, HTTPException, UploadFile, File as FileBody
import httpx
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from src.middleware.engine import AsyncSession
from src.fastkit.services.base import BaseService
from .repository import TripRepository, TripImageRepository
from .models.trip import Trip, TripImage
from .schemas.trip import TripCreate, TripResponse
from src.app.files.service import FileService
from src.app.files.register import get_file_service


class TripService(BaseService[Trip]):
    """Сервис для работы с поездками, поддерживающий загрузку изображений."""

    def __init__(self, db_session: AsyncSession, ):
        super().__init__(TripRepository(db_session))
        self.trip_image_repository = TripImageRepository(db_session)
        self.db_session = db_session

    async def create_with_images(
        self, request: Request, trip_data: TripCreate, images: Optional[List[UploadFile]] = None
    ) -> TripResponse:
        """Создаёт поездку и загружает изображения через локальный API."""

        async with self.repository.uow.transaction():
            trip = await self.create(trip_data)

            image_urls = []
            if images:
                image_urls = await self._upload_images_via_api(request, images)

            # Сохраняем ссылки на изображения
            await self.trip_image_repository.create_many(
                [TripImage(trip_id=trip.id, image_url=url) for url in image_urls]
            )

            return TripResponse(
                id=trip.id,
                title=trip.title,
                images=image_urls
            )

    async def _upload_images_via_api(
        self, request: Request, images: List[UploadFile]
    ) -> List[str]:
        """Отправляет файлы в локальный API FastAPI и получает их ID."""

        async with httpx.AsyncClient(base_url="http://0.0.0.0:8000") as client:
            image_urls = []
            for image in images:
                form = {"file": (image.filename, await image.read(), image.content_type)}
                response = await client.post("/files/upload", files=form)

                if response.status_code == 200:
                    file_id = response.json()["id"]
                    image_urls.append(f"http://0.0.0.0:8000/files/{file_id}/decoded")
                else:
                    raise Exception(f"Ошибка загрузки файла: {response.text}")

        return image_urls
