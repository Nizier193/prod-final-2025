# DTO (Pydantic Models)

from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID


# Same for AdvertiserUpsert (No Difference at all)
class Advertiser(BaseModel):
    # Объект, представляющий клиента системы.

    advertiser_id: UUID = Field(..., description="Уникальный идентификатор.")
    name: str = Field(..., description="Название рекламодателя.")



# Class for ML Scores
class MLScore(BaseModel):
    # Объект с данными ML скора, включая client_id, advertiser_id и значение скора.
    
    client_id: UUID = Field(..., description="UUID клиента.")
    advertiser_id: UUID = Field(..., description="UUID рекламодателя.")
    score: int = Field(..., description="ML Score пары.")