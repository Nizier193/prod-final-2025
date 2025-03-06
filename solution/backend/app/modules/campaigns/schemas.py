# Модели для БД

from sqlalchemy import Float, Column, Integer, String, UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass


class Campaign(Base):
    __tablename__ = "campaigns"

    campaign_id = Column("campaign_id", UUID, primary_key=True)
    advertiser_id = Column("advertiser_id", UUID)
    impressions_limit = Column("impressions_limit", Integer)
    clicks_limit = Column("clicks_limit", Integer)
    cost_per_impression = Column("cost_per_impression", Float)
    cost_per_click = Column("cost_per_click", Float)
    ad_title = Column("ad_title", String)
    ad_text = Column("ad_text", String)
    start_date = Column("start_date", Integer)
    end_date = Column("end_date", Integer)

    targeting = relationship(
        "Targeting", 
        back_populates="campaign", 
        uselist=False, 
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{self.to_dict()}"


    def to_dict(self):
        # Преобразуем основные поля Campaign в словарь
        model_dict = {
            "campaign_id": self.campaign_id,
            "advertiser_id": self.advertiser_id,
            "impressions_limit": self.impressions_limit,
            "clicks_limit": self.clicks_limit,
            "cost_per_impression": self.cost_per_impression,
            "cost_per_click": self.cost_per_click,
            "ad_title": self.ad_title,
            "ad_text": self.ad_text,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

        if model_dict.get("targeting"):
            model_dict["targeting"] = {
                "gender": self.targeting.gender,
                "age_from": self.targeting.age_from,
                "age_to": self.targeting.age_to,
                "location": self.targeting.location,
            }

        return model_dict


class Targeting(Base):
    __tablename__ = "targeting"

    campaign_id = Column("campaign_id", UUID, ForeignKey("campaigns.campaign_id"), primary_key=True)
    gender = Column("gender", String, nullable=True)
    age_from = Column("age_from", Integer, nullable=True)
    age_to = Column("age_to", Integer, nullable=True)
    location = Column("location", String, nullable=True)

    # Отношение "один к одному" с таблицей campaigns
    campaign = relationship("Campaign", back_populates="targeting")

    def to_dict(self):
        return {
            "gender": self.gender,
            "age_from": self.age_from,
            "age_to": self.age_to,
            "location": self.location
        }


from core.database import get_db
Base.metadata.drop_all(next(get_db()).bind)