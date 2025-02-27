from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.middleware.engine import Base

class Trip(Base):
    """Модель поездки (экскурсии)."""
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    idea = Column(String, nullable=True)
    route = Column(String, nullable=True)
    themes = Column(String, nullable=True)
    facts = Column(String, nullable=True)
    suitable_for = Column(String, nullable=True)
    details = Column(String, nullable=True)
    meeting_point = Column(String, nullable=True)
    questions = Column(String, nullable=True)

    images = relationship("TripImage", back_populates="trip", cascade="all, delete")


class TripImage(Base):
    """Модель изображения поездки (с хранением URL, а не base64)."""
    __tablename__ = "trip_images"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String, nullable=False)  # Сохраняем ссылку на изображение

    trip = relationship("Trip", back_populates="images")