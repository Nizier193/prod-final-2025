import json
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

class Config(BaseSettings):
    HOST: str
    PORT: int
    DATABASE_URI: str
    CACHE_HOST: str
    CACHE_PORT: int
    OPENAI_API_KEY: str
    OPENAI_BASEURL: str
    OPENROUTER_MODEL: str
    S3_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str

    class Config:
        env_file = ".env"  # Указываем, откуда брать переменные

config = Config()
