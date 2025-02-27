from pydantic import BaseModel
from typing import List, Optional

class TripImageRead(BaseModel):
    """Ответ с изображением."""
    id: int
    image_url: str  # Теперь это ссылка, а не base64

    class Config:
        from_attributes = True

class TripCreate(BaseModel):
    """Схема создания поездки."""
    title: str
    idea: Optional[str] = None
    route: Optional[str] = None
    themes: Optional[str] = None
    facts: Optional[str] = None
    suitable_for: Optional[str] = None
    details: Optional[str] = None
    meeting_point: Optional[str] = None
    questions: Optional[str] = None
    images: List[str] = []  # Тут список URL изображений

class TripRead(TripCreate):
    """Схема ответа на запрос поездки."""
    id: int
    images: List[TripImageRead] = []  # Ответ с ID и ссылками

    class Config:
        from_attributes = True