from pydantic import BaseModel
from typing import Optional, Dict


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
    base64_data: str

    class Config:
        from_attributes = True
