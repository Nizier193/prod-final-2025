import json
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

class Config(BaseSettings):
    BACKEND_BASEURL: str

    class Config:
        env_file = ".env"  # Указываем, откуда брать переменные

config = Config()
