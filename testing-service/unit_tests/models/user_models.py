# DTO (Pydantic Models)

from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID


# Same for ClientUpsert (No Difference at all)
class Client(BaseModel):
    # Объект, представляющий клиента системы.

    client_id: UUID = Field(..., description="Уникальный идентификатор клиента (UUID).")
    login: str = Field(..., description="Логин клиента в системе.")
    age: int = Field(..., description="Возраст клиента.")
    location: str = Field(..., description="Локация клиента (город, регион или район).")
    gender: str = Field(..., description="Пол клиента (MALE или FEMALE).")