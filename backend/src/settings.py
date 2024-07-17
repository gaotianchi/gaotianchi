import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent


class BaseConfig:
    SECRET_KEY = b"0yy0lYd6o4Yqv3v99kt1J7VtJRbq44z8CVkTBw3Aagg="


class V1(BaseConfig):
    VERSION = "1"
    DATA_ROOT_FOLDER = ROOT.joinpath("data", "v1")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
        DATA_ROOT_FOLDER.joinpath("data.v1.db")
    )
    UPLOAD_FOLDER = DATA_ROOT_FOLDER.joinpath("uploads")
    RESUME_FOLDER = DATA_ROOT_FOLDER.joinpath("resumes")
    NUMBER_OF_PAGE_TWEETS = 3
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


class V2(BaseConfig):
    VERSION = "2"
    DATA_ROOT_FOLDER = ROOT.joinpath("data", "v2")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
        DATA_ROOT_FOLDER.joinpath("data.v2.db")
    )
    PHOTO_FOLDER = DATA_ROOT_FOLDER.joinpath("photos")
    RESUME_PATH = DATA_ROOT_FOLDER.joinpath("resume.pdf")
    NUMBER_OF_PAGE_TWEETS = 2
    if not DATA_ROOT_FOLDER.exists():
        DATA_ROOT_FOLDER.mkdir(exist_ok=True)
    if not PHOTO_FOLDER.exists():
        PHOTO_FOLDER.mkdir(exist_ok=True)


class TestingConfig(BaseConfig): ...


def get_config(version: str | None = None):
    version = version if version else os.getenv("VERSION")
    match version:
        case "1":
            return V1
        case "2":
            return V2
        case "testing":
            return TestingConfig
        case _:
            return V1
