from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from src.flaskextens import db


class Me(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    author_name: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    profile: Mapped[str] = mapped_column(Text)
    registered_at: Mapped[datetime] = mapped_column(DateTime)
    blog_title: Mapped[str] = mapped_column(String(255))
    blog_sub_title: Mapped[str] = mapped_column(String(255))
    resume: Mapped[str] = mapped_column(String(255))
    tweets: Mapped[List["Tweet"]] = relationship(back_populates="me")
    photos: Mapped[List["Photo"]] = relationship(back_populates="me")

    @classmethod
    def post_me(cls, username: str, password: str) -> "Me":
        me = Me(
            username=username,
            author_name=username,
            password_hash=generate_password_hash(password),
            profile=f"我是 {username}，欢迎来到我的个人网站。",
            registered_at=datetime.now(),
            blog_title=f"{username} 的个人网站",
            blog_sub_title="",
            resume="",
        )  # type: ignore
        db.session.add(me)
        db.session.commit()
        return Me.query.get(me.id)  # type: ignore

    def patch_me(
        self,
        author_name: str,
        profile: str,
        blog_title: str,
        blog_sub_title: str,
        resume: str,
    ) -> "Me":
        self.author_name = author_name
        self.profile = profile
        self.blog_title = blog_title
        self.blog_sub_title = blog_sub_title
        self.resume = resume
        db.session.add(self)
        db.session.commit()
        return Me.query.get(self.id)  # type: ignore

    def validate_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Tweet(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    photos: Mapped[List["Photo"]] = relationship(back_populates="tweet")
    me: Mapped[Me] = relationship(back_populates="tweets")
    me_id: Mapped[int] = mapped_column(ForeignKey("me.id"))

    @classmethod
    def post_tweet(cls, text: str, me_id: int) -> "Tweet":
        tweet = Tweet(text=text, me_id=me_id, created_at=datetime.now())  # type: ignore
        db.session.add(tweet)
        db.session.commit()

        return Tweet.query.get(tweet.id)  # type: ignore

    def patch_tweet(self, text: str) -> "Tweet":
        self.text = text
        db.session.add(self)
        db.session.commit()
        return Tweet.query.get(self.id)  # type: ignore

    def delete(self):
        for p in self.photos:
            db.session.delete(p)
        db.session.commit()
        db.session.delete(self)
        db.session.commit()


class Photo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255))
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweet.id"))
    tweet: Mapped[Tweet] = relationship(back_populates="photos")
    me: Mapped[Me] = relationship(back_populates="photos")
    me_id: Mapped[int] = mapped_column(ForeignKey("me.id"))

    @classmethod
    def post_me(cls, filename: str, tweet_id: int, me_id: int) -> "Photo":
        photo = Photo(
            filename=filename,
            tweet_id=tweet_id,
            me_id=me_id,
        )  # type: ignore

        db.session.add(photo)
        db.session.commit()
        return Photo.query.get(photo.id)  # type: ignore
