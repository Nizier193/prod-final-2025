# DTO (Pydantic Models)

from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID


# Targeting
class Targeting(BaseModel):
    # Объект, описывающий настройки таргетирования для рекламной кампании.
    gender: Optional[str] = Field(None, description="Пол (м-т быть ALL)")
    age_from: Optional[int] = Field(None, description="Минимальный включительно возраст")
    age_to: Optional[int] = Field(None, description="Минимальный включительно возраст")
    location: Optional[str] = Field(None, description="Локация аудитории.")


# Класс возвращаемый HTTP запросами
class Campaign(BaseModel):
    campaign_id: UUID = Field(..., description="UUID кампании")
    advertiser_id: UUID = Field(..., description="UUID владельца кампании")
    impressions_limit: int = Field(..., description="Лимит показов рекламного объявления (фиксируется до старта кампании).")
    clicks_limit: int = Field(..., description="Лимит переходов (кликов) по рекламному объявлению (фиксируется до старта кампании).")
    cost_per_impression: float = Field(..., description="Стоимость одного показа рекламного объявления.")
    cost_per_click: float = Field(..., description="Стоимость одного перехода (клика) по рекламному объявлению.")
    ad_title: str = Field(..., description="Название рекламного объявления.")
    ad_text: str = Field(..., description="Текст рекламного объявления.")
    start_date: int = Field(..., description="День старта показа рекламного объявления (включительно).")
    end_date: int = Field(..., description="День окончания показа рекламного объявления (включительно).")
    targeting: Targeting = Field(...)



# Моделька, где Targeting - необязателен
class CampaignCreate(BaseModel):
    impressions_limit: int  = Field(..., description="Лимит")
    clicks_limit: int = Field(...)
    cost_per_impression: float = Field(...)
    cost_per_click: float = Field(...)
    ad_title: str = Field(...)
    ad_text: str = Field(...)
    start_date: int = Field(...)
    end_date: int = Field(...)
    targeting: Optional[Targeting] = Field(Targeting())


# Моделька с необязательными полями
class CampaignUpdate(BaseModel):
    impressions_limit: Optional[int] = Field(None)
    clicks_limit: Optional[int] = Field(None)
    cost_per_impression: Optional[float] = Field(None)
    cost_per_click: Optional[float] = Field(None)
    ad_title: Optional[str] = Field(None)
    ad_text: Optional[str] = Field(None)
    start_date: Optional[int] = Field(None)
    end_date: Optional[int] = Field(None)
    targeting: Optional[Targeting] = Field(None)
