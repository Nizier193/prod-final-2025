# DTO (Pydantic Models)

from pydantic import BaseModel, Field, model_validator
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
    score: int = Field(default=0, strict=True, ge=0, description="ML Score пары.")

    @model_validator(mode="after")
    def validate_score(self):
        if self.score == None:
            self.score = 0

        return self
