import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent


class BaseConfig:
    SECRET_KEY = b"0yy0lYd6o4Yqv3v99kt1J7VtJRbq44z8CVkTBw3Aagg="
    UPLOAD_FOLDER = ROOT.joinpath("data", "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    NUMBER_OF_PAGE_TWEETS = 2


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(ROOT.joinpath("data", "data.dev.db"))


class ProductionConfig(BaseConfig): ...


class TestingConfig(BaseConfig): ...


def get_config(environment: str | None = None):
    environment = environment if environment else os.getenv("ENVIRONMENT")
    match environment:
        case "development":
            return DevelopmentConfig
        case "production":
            return ProductionConfig
        case "testing":
            return TestingConfig
        case _:
            return DevelopmentConfig
