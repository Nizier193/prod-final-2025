# DTO (Pydantic Models)

from pydantic import BaseModel, Field, model_validator

class Stats(BaseModel):
    impressions_count: int = Field(0, description="Количество просмотров")
    clicks_count: int = Field(0, description="Количество кликов")
    conversion: float = Field(0, description="Конверсия")
    spent_impressions: float = Field(0, description="Сумма денег, потраченная на показы")
    spent_clicks: float = Field(0, description="Сумма денег, потраченная на переходы")
    spent_total: float = Field(0, description="Общая сумма денег, потраченная на показы и клики.")

class DailyStats(Stats):
    date: int = Field(0, description="День, за к-й собрана стата.")


# DTO (Pydantic Models)

from typing import Optional
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from uuid import UUID

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ALL = "ALL"


# Targeting
class Targeting(BaseModel):
    # Объект, описывающий настройки таргетирования для рекламной кампании.
    gender: Optional[Gender] = Field(None, description="Пол (м-т быть ALL)")
    age_from: Optional[int] = Field(None, strict=True, description="Минимальный включительно возраст")
    age_to: Optional[int] = Field(None, strict=True, description="Минимальный включительно возраст")
    location: Optional[str] = Field(None, strict=True, description="Локация аудитории.")


    @model_validator(mode="after")
    def validate_targeting(self):
        if (self.age_from and self.age_to):
            if (self.age_from > self.age_to):
                raise Exception("age_to is greater that age_from")
        return self


    def to_dict(self):
        model_dict = self.model_dump()
        gender = self.gender
        model_dict["gender"] = gender.value if gender else None
        return model_dict


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

    def moderate_text(self, moderator) -> bool:
        title_status, self.ad_title = moderator.moderate_naive(self.ad_title)
        text_status, self.ad_text = moderator.moderate_naive(self.ad_text)

        if (not title_status) or (not text_status):
            return False
           
        return True

    def to_dict(self):
        model_dict = self.model_dump()
        model_dict["targeting"] = self.targeting.to_dict()
        return model_dict


# Моделька, где Targeting - необязателен
class CampaignCreate(BaseModel):
    impressions_limit: int  = Field(..., ge=0, description="Лимит")
    clicks_limit: int = Field(..., ge=0, strict=True)
    cost_per_impression: float = Field(..., ge=0, strict=True)
    cost_per_click: float = Field(..., ge=0, strict=True)
    ad_title: str = Field(..., strict=True)
    ad_text: str = Field(..., strict=True)
    start_date: int = Field(..., ge=0, strict=True)
    end_date: int = Field(..., ge=0, strict=True)
    targeting: Optional[Targeting] = Field(Targeting())

    @model_validator(mode='after')
    def validate_model(self):
        if (self.start_date > self.end_date):
            raise Exception("Start date is greater than end date.")
        return self


# Моделька с необязательными полями
class CampaignUpdate(BaseModel):
    impressions_limit: int = Field(...)
    clicks_limit: int = Field(...)
    cost_per_impression: float = Field(...)
    cost_per_click: float = Field(...)
    ad_title: str = Field(...)
    ad_text: str = Field(...)
    start_date: int = Field(...)
    end_date: int = Field(...)
    targeting: Optional[Targeting] = Field(Targeting()) # Опционален только Targeting - его меняем на null если чет не сходится


    def to_dict(self):
        model_dict = self.model_dump()
        targeting = self.targeting
        model_dict["targeting"] = targeting.to_dict() if targeting else None
        return model_dict
    
    
    def moderate_text(self, moderator) -> bool:
        title_status, self.ad_title = moderator.moderate_naive(self.ad_title)
        text_status, self.ad_text = moderator.moderate_naive(self.ad_text)

        if (not title_status) or (not text_status):
            return False
           
        return True


    @model_validator(mode='after')
    def validate_model(self):
        if (self.start_date > self.end_date):
            raise Exception("Start date is greater than end date.")

        return self
    