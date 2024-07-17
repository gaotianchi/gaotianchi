from flask import Blueprint, current_app, jsonify, send_file

from src.apis.v2.database import Me, Photo, Tweet
from src.apis.v2.serializer import get_my_detail, get_my_profile, get_tweet_detail
from src.utlis import abort

visitor = Blueprint("visitor", __name__)


@visitor.route("/resume")
def get_resume_url():
    return send_file(current_app.config["RESUME_PATH"])


@visitor.route("/photo/<filename>")
def get_photo_url(filename: str):
    return send_file(current_app.config["PHOTO_FOLDER"].joinpath(filename))


@visitor.route("/my-profile")
def get_profile():
    me = Me.query.first()

    return jsonify(get_my_profile(me)), 200  # type: ignore


@visitor.route("/my-detail")
def get_detail():
    me = Me.query.first()
    return jsonify(get_my_detail(me)), 200  # type: ignore


@visitor.route("/page-tweets/<int:page>")
def get_page_tweets(page: int):
    pagination = Tweet.query.order_by(Tweet.created_at.desc()).paginate(page=page, per_page=current_app.config["NUMBER_OF_PAGE_TWEETS"])  # type: ignore
    tweets = [get_tweet_detail(t) for t in pagination.items]
    return tweets, 200


@visitor.route("/tweets")
def get_latest_tweet():
    tweet = Tweet.query.order_by(Tweet.created_at.desc()).first()  # type: ignore
    if not tweet:
        return abort("No tweet found", 404)
    return jsonify(get_tweet_detail(tweet)), 200  # type: ignore
