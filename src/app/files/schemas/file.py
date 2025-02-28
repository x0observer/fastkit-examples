from enum import Enum
from pydantic import BaseModel



class ALLOWED_CONTENT_TYPES(str, Enum):
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_GIF = "image/gif"
    APPLICATION_PDF = "application/pdf"


class FileCreate(BaseModel):
    filename: str
    content_type: str = None

    # class Config:
    #     from_attributes = True


class FileRead(FileCreate):
    id: int

    # class Config:
    #     from_attributes = True
    

class FileUploadResponse(BaseModel):
    """Schema for file response."""

    id: int
    filename: str
    content_type: str

    class Config:
        from_attributes = True
