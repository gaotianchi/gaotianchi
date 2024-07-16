from flask import url_for

from src.apis.v1.database import Photo, Resume, Tweet, User
from src.utlis import serialize_datetime

#################### resume #############################


def get_resume_profile(r: Resume):
    url = url_for("v1.visitor.get_a_resume", filename=r.filename, _external=True)
    return {"id": r.id, "filename": r.filename, "url": url, "userId": r.user_id}


def get_resume_detail(r: Resume):
    url = url_for("v1.visitor.get_a_resume", filename=r.filename, _external=True)
    return {
        "id": r.id,
        "filename": r.filename,
        "url": url,
        "userProfile": get_user_profile(r.user),
    }


######################## photo ################################


def get_photo_profile(photo: Photo):
    url = url_for("v1.visitor.get_a_photo", filename=photo.filename, _external=True)
    return {
        "id": photo.id,
        "url": url,
        "tweetId": photo.tweet_id,
        "userId": photo.user_id,
    }


def get_photo_detail(p: Photo):
    url = url_for("v1.visitor.get_a_photo", filename=p.filename, _external=True)
    t_profile = get_tweet_profile(p.tweet)
    u_profile = get_user_profile(p.user)
    filename = p.filename
    return {
        "id": p.id,
        "url": url,
        "tweetProfile": t_profile,
        "userProfile": u_profile,
        "filename": filename,
    }


########################## tweet #################################


def get_tweet_profile(t: Tweet):
    return {
        "id": t.id,
        "text": t.text[:50],
        "createdAt": serialize_datetime(t.created_at),
        "userId": t.user_id,
    }


def get_tweet_detail(t: Tweet):
    return {
        "id": t.id,
        "text": t.text,
        "createdAt": serialize_datetime(t.created_at),
        "userProfile": get_user_profile(t.user),
        "photoProfiles": [get_photo_profile(p) for p in t.photos],
    }


############################ user ##################################


def get_user_profile(u: User):
    return {
        "id": u.id,
        "username": u.username,
        "profile": u.profile,
        "registerAt": serialize_datetime(u.registered_at),
    }


def get_user_detail(u: User):
    return {
        "id": u.id,
        "username": u.username,
        "profile": u.profile,
        "registerAt": serialize_datetime(u.registered_at),
        "tweetProfiles": [get_tweet_profile(t) for t in u.tweets[:30]],
        "photoProfiles": [get_photo_profile(p) for p in u.photos[:50]],
        "resumeProfile": get_resume_profile(u.resume),
    }


############################ token ##################################33


def get_token_response_data(access_token: str, token_type: str):
    return {"accessToken": access_token, "tokenType": token_type}
