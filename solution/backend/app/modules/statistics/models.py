# DTO (Pydantic Models)

from pydantic import BaseModel, Field, model_validator
from uuid import UUID


class Ad(BaseModel):
    ad_id: UUID = Field(..., description="Уникальный идентификатор рекламного объявления (всегда совпадает с id рекламной кампании).")
    ad_title: str = Field(..., description="Название рекламного объявления.")
    ad_text: str = Field(..., description="Текст рекламного объявления, который видит клиент.")
    advertiser_id: UUID = Field(..., description="UUID рекламодателя, которому принадлежит объявление.")


class Stats(BaseModel):
    impressions_count: int = Field(0, description="Количество просмотров")
    clicks_count: int = Field(0, description="Количество кликов")
    conversion: float = Field(0, description="Конверсия")
    spent_impressions: float = Field(0, description="Сумма денег, потраченная на показы")
    spent_clicks: float = Field(0, description="Сумма денег, потраченная на переходы")
    spent_total: float = Field(0, description="Общая сумма денег, потраченная на показы и клики.")


    # Магическая функция для автоматического заполнения конверсии
    @model_validator(mode='after')
    def calculate_derived_fields(self):
        if self.impressions_count > 0:
            self.conversion = (self.clicks_count / self.impressions_count) * 100
        self.spent_total = self.spent_impressions + self.spent_clicks
        return self

    # Магическая функция для складывания статистик
    def __add__(self, other_stat):
        return Stats(
            impressions_count=self.impressions_count + other_stat.impressions_count,
            clicks_count=self.clicks_count + other_stat.clicks_count,
            spent_impressions=self.spent_impressions + other_stat.spent_impressions,
            spent_clicks=self.spent_clicks + other_stat.spent_clicks
        )
        


class DailyStats(Stats):
    date: int = Field(0, description="День, за к-й собрана стата.")

    