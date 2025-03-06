from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    BACKEND_BASEURL: str
    TELEGRAM_TOKEN: str
    PATH_TO_SOURCES: str = "unit_tests/resources"

    class ConfigDict:
        env_file = ".env"


config = Config()

config.BACKEND_BASEURL = "http://localhost:8080"