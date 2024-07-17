from flask import jsonify, url_for

from src.utlis import serialize_datetime

from .database import *


def get_token_response_data(access_token: str, token_type: str):
    return {"accessToken": access_token, "tokenType": token_type}


def get_my_profile(me: Me):
    return {
        "id": me.id,
        "username": me.username,
        "authorName": me.author_name,
        "profile": me.profile,
        "registerAt": serialize_datetime(me.registered_at),
        "blogTitle": me.blog_title,
        "blogSubTitle": me.blog_sub_title,
        "resume": me.resume,
    }


def get_tweet_profile(t: Tweet):
    return {
        "id": t.id,
        "text": t.text[:50],
        "createdAt": serialize_datetime(t.created_at),
        "meId": t.me_id,
    }


def get_photo_profile(p: Photo):
    url = url_for("v2.visitor.get_photo_url", filename=p.filename, _external=True)
    return {
        "id": p.id,
        "url": url,
        "tweetId": p.tweet_id,
        "meId": p.me_id,
    }


def get_my_detail(me: Me):
    return {
        "id": me.id,
        "username": me.username,
        "authorName": me.author_name,
        "profile": me.profile,
        "registerAt": serialize_datetime(me.registered_at),
        "blogTitle": me.blog_title,
        "blogSubTitle": me.blog_sub_title,
        "resume": url_for("v2.visitor.get_resume_url", _external=True),
        "tweetProfiles": [get_tweet_profile(t) for t in me.tweets],
        "photoProfiles": [get_photo_profile(p) for p in me.photos],
    }


def get_tweet_detail(t: Tweet):
    return {
        "id": t.id,
        "text": t.text,
        "createdAt": serialize_datetime(t.created_at),
        "myProfile": get_my_profile(t.me),
        "photoProfiles": [get_photo_profile(p) for p in t.photos],
    }


def get_photo_detail(p: Photo):
    return {
        "id": p.id,
        "url": url_for("v2.visitor.get_photo_url", filename=p.filename, _external=True),
        "tweetProfile": get_tweet_profile(p.tweet),
        "meProfile": get_my_profile(p.me),
    }
