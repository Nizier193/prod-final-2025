# DTO (Pydantic Models)

from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


# Same for ClientUpsert (No Difference at all)
class Client(BaseModel):
    # Объект, представляющий клиента системы.

    client_id: UUID = Field(..., description="Уникальный идентификатор клиента (UUID).")
    login: str = Field(..., description="Логин клиента в системе.")
    age: int = Field(..., gt=0, le=100, strict=True, description="Возраст клиента.")
    location: str = Field(..., description="Локация клиента (город, регион или район).")
    gender: Gender = Field(..., description="Пол клиента (MALE или FEMALE).")

    def to_dict(self):
        model_dict = self.model_dump()

        model_dict["gender"] = self.gender.value
        return model_dict