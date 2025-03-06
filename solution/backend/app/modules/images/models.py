# DTO (Pydantic Models)

from typing import Optional
from pydantic import BaseModel, Field


class ImageModel(BaseModel):
    key: Optional[str] = None
    url: Optional[str] = None
    status: bool = Field(..., description="Статус добавления")
