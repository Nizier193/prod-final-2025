from typing import List, Union
from pydantic import BaseModel, Field

from src.models.text_templates.templates import view_ad_template, click_ad_template

class ClickAdResponse(BaseModel):
    ad_id: str = Field(..., description="ID рекламы.")
    advertiser_name: str = Field(..., description="Имя рекламодателя.")
    ad_title: str = Field(..., description="Заголовок рекламы.")
    ad_text: str = Field(..., description="Текст рекламы.")
    remains_active: Union[int, str] = Field(..., description="Сколько будет ещё активно в днях (с даты установленной на сервере).")
    image_urls: List[str] = Field(..., description="Ссылки на картинки на сервере.")

    def to_str(self):
        return click_ad_template.format(
            advertiser_name=self.advertiser_name,
            ad_title=self.ad_title,
            ad_text=self.ad_text,
            remains_active=self.remains_active,
            image_urls="\n\n".join([url for url in self.image_urls])
        )


class ViewAdResponse(BaseModel):
    ad_id: str = Field(..., description="ID рекламы.")
    advertiser_name: str = Field(..., description="Имя рекламодателя.")
    ad_title: str = Field(..., description="Заголовок рекламы.")
    ad_text: str = Field(..., description="Текст рекламы.")

    def to_str(self):
        return view_ad_template.format(
            advertiser_name=self.advertiser_name,
            ad_title=self.ad_title,
            ad_text=self.ad_text[:40] + "..."
        )


class ClickResponse(BaseModel):
    status: bool = Field(..., description="Статус клика. (Кликнул или нет).")
    message: str = Field(..., description="Сообщение для пользователя.")

    