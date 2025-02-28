
from pydantic import BaseModel, Field
from typing import List, Optional


class TripImageRead(BaseModel):
    """Ответ с изображением."""
    id: int
    image_url: str  # Теперь это ссылка, а не base64

    class Config:
        from_attributes = True

class TripCreate(BaseModel):
    """
    Схема запроса для создания поездки.
    
    Атрибуты:
        title (str): Название поездки. Обязательное поле.
        idea (Optional[str]): Краткое описание идеи путешествия.
        route (Optional[str]): Маршрут поездки.
        themes (Optional[str]): Тематические направления (например, "приключения, история").
        facts (Optional[str]): Интересные факты о путешествии.
        suitable_for (Optional[str]): Для кого подходит поездка (например, "семьи, любители активного отдыха").
        details (Optional[str]): Подробное описание программы.
        meeting_point (Optional[str]): Место встречи перед началом поездки.
        questions (Optional[str]): Часто задаваемые вопросы.
    """

    title: str = Field(..., min_length=3, max_length=255, description="Название поездки")
    idea: Optional[str] = Field(None, max_length=500, description="Краткое описание идеи путешествия")
    route: Optional[str] = Field(None, max_length=1000, description="Описание маршрута")
    themes: Optional[str] = Field(None, max_length=500, description="Темы путешествия (через запятую)")
    facts: Optional[str] = Field(None, max_length=1000, description="Интересные факты о маршруте")
    suitable_for: Optional[str] = Field(None, max_length=500, description="Для кого подходит путешествие")
    details: Optional[str] = Field(None, max_length=5000, description="Детальное описание программы поездки")
    meeting_point: Optional[str] = Field(None, max_length=255, description="Место встречи перед началом поездки")
    questions: Optional[str] = Field(None, max_length=1000, description="Часто задаваемые вопросы")

    class Config:
        """Дополнительные настройки модели."""
        json_schema_extra = {
            "example": {
                "title": "Экспедиция на Камчатку",
                "idea": "Уникальное приключение по вулканам и гейзерам Камчатки.",
                "route": "Петропавловск-Камчатский → Долина гейзеров → вулкан Толбачик",
                "themes": "приключения, природа, экстрим",
                "facts": "В маршруте — крупнейший вулканический массив Камчатки.",
                "suitable_for": "Любители активного отдыха, фотографы, геологи",
                "details": "7-дневная поездка с восхождением на вулканы, термальными источниками и вертолетными экскурсиями.",
                "meeting_point": "Аэропорт Петропавловска-Камчатского",
                "questions": "Что взять с собой? Нужно ли специальное снаряжение?"
            }
        }
    # images: List[str] = []  # Тут список URL изображений

class TripRead(TripCreate):
    """Схема ответа на запрос поездки."""
    id: int
    # images: List[TripImageRead] = []  # Ответ с ID и ссылками

    class Config:
        from_attributes = True
        
        
class TripResponse(TripRead):

    images: List[str] = []