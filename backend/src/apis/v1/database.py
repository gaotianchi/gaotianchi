from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from src.flaskextens import db
from src.settings import get_config


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    profile: Mapped[str] = mapped_column(Text)
    registered_at: Mapped[datetime] = mapped_column(DateTime)
    tweets: Mapped[List["Tweet"]] = relationship(back_populates="user")
    photos: Mapped[List["Photo"]] = relationship(back_populates="user")
    resume: Mapped["Resume"] = relationship(back_populates="user")

    @classmethod
    def create(cls, username: str, password: str) -> "User":
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            registered_at=datetime.now(),
            profile=f"我是 {username}，欢迎来到我的个人网站。",
        )  # type: ignore

        db.session.add(user)
        db.session.commit()
        return User.query.get(user.id)  # type: ignore

    def update_profile(self, profile: str) -> "User":
        self.profile = profile
        db.session.add(self)
        db.session.commit()
        return User.query.get(self.id)  # type: ignore

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def validate_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Resume(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="resume")

    @classmethod
    def create(cls, filename: str, user_id: int) -> "Resume":
        resume = Resume(filename=filename, user_id=user_id)  # type: ignore
        db.session.add(resume)
        db.session.commit()

        return Resume.query.get(resume.id)  # type: ignore

    def update(self, filename: str) -> "Resume":
        self.filename = filename
        db.session.add(self)
        db.session.commit()
        return Resume.query.get(self.id)  # type: ignore


class Tweet(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    photos: Mapped[List["Photo"]] = relationship(back_populates="tweet")  # type: ignore
    user: Mapped[User] = relationship(back_populates="tweets")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    @classmethod
    def create(cls, text: str, user_id: int) -> "Tweet":
        tweet = Tweet(
            text=text, user_id=user_id, created_at=datetime.now()
        )  # type: ignore
        db.session.add(tweet)
        db.session.commit()

        return Tweet.query.get(tweet.id)  # type: ignore

    def update(self, text: str) -> "Tweet":
        self.text = text
        db.session.add(self)
        db.session.commit()
        return Tweet.query.get(self.id)  # type: ignore

    def delete(self):
        config = get_config()
        for p in self.photos:
            path = config.PHOTO_FOLDER.joinpath(p.filename)
            path.unlink()
            db.session.delete(p)
        db.session.commit()
        db.session.delete(self)
        db.session.commit()


class Photo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255))
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweet.id"))
    tweet: Mapped[Tweet] = relationship(back_populates="photos")
    user: Mapped[User] = relationship(back_populates="photos")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    @classmethod
    def create(cls, filename: str, tweet_id: int, user_id: int) -> "Photo":
        photo = Photo(
            filename=filename,
            tweet_id=tweet_id,
            user_id=user_id,
        )  # type: ignore

        db.session.add(photo)
        db.session.commit()
        return Photo.query.get(photo.id)  # type: ignore

    def delete(self):
        config = get_config()
        path = config.PHOTO_FOLDER.joinpath(self.filename)
        path.unlink()
        db.session.delete(self)
        db.session.commit()
