# DTO (Pydantic Models)

from pydantic import BaseModel, Field


# Установка времени
class TimeAdvance(BaseModel):
    current_date: int = Field(..., strict=True, description="Новая дата.")