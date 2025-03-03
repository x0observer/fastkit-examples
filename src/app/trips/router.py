

from typing import List, Type
from fastapi import UploadFile, File, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.fastkit.routers.base import BaseRouter
from src.middleware.engine import get_async_session
from src.app.trips.models.trip import Trip
from src.app.trips.schemas.trip import TripCreate, TripRead, TripResponse
from src.app.trips.service import TripService

class TripRouter(BaseRouter[Trip, TripCreate, TripRead]):
    """Маршрут для работы с поездками."""

    def __init__(self, service_cls: Type[TripService], prefix: str): #file_service: FileService):
        super().__init__(service_cls, prefix, TripCreate, TripRead)
        # self.file_service = file_service
        

        @self.router.post("/create-with-images", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
        async def create_with_images(
            trip_data: TripCreate = Depends(),
            images: List[UploadFile] = File(None),
            db_session: AsyncSession = Depends(get_async_session),
        ):
            """
            Создаёт поездку с изображениями.
            Файлы передаются как multipart/form-data.
            """
            service = self.service_cls(db_session)

            # Создаём поездку с изображениями
            trip = await service.create_with_images(trip_data=trip_data, images=images)

            return TripResponse.model_validate(trip, from_attributes=True)
