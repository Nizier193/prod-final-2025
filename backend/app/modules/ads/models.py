# DTO (Pydantic Models)

from pydantic import BaseModel, Field
from uuid import UUID


class Ad(BaseModel):
    ad_id: UUID = Field(..., description="Уникальный идентификатор рекламного объявления (всегда совпадает с id рекламной кампании).")
    ad_title: str = Field(..., description="Название рекламного объявления.")
    ad_text: str = Field(..., description="Текст рекламного объявления, который видит клиент.")
    advertiser_id: UUID = Field(..., description="UUID рекламодателя, которому принадлежит объявление.")
