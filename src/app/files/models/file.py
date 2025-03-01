from sqlalchemy import Column, Integer, String, JSON
from src.middleware.engine import Base

class File(Base):
    """
    Represents a file entity in the database.
    Stores metadata and base64-encoded file content.
    """
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    file_metadata = Column(JSON, nullable=True)  # JSONB field to store metadata
    base64_data = Column(String, nullable=True)  # Stores base64-encoded file data