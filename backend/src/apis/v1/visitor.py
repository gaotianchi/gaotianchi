from pathlib import Path
from typing import cast

from flask import Blueprint, current_app, jsonify, send_file

from src.apis.v1.database import Photo, Tweet
from src.utlis import abort

from .apis import *

visitor = Blueprint("visitor", __name__)

########################## user ###########################3###


@visitor.route("/users/<username>")
def get_a_user(username: str):
    user = User.query.filter_by(username=username).first()  # type: ignore
    if not user:
        return abort("No user found.", 404)
    return jsonify(get_user_profile(user)), 200  # type: ignore


@visitor.route("/users")
def get_admin_profile():
    user = User.query.first()  # type: ignore
    return jsonify(get_user_profile(user)), 200  # type: ignore


######################## photo #####################################


@visitor.route("/photos/<filename>")
def get_a_photo(filename: str):
    photo = Photo.query.filter_by(filename=filename).first()  # type: ignore
    if not photo:
        return abort("No photo found.", 404)
    return send_file(current_app.config["UPLOAD_FOLDER"].joinpath(filename))  # type: ignore


######################### resume ################################


@visitor.route("/resume/<filename>")
def get_a_resume(filename: str):
    resume = cast(Resume, Resume.query.filter_by(filename=filename).first())
    if not resume:
        return abort("No resume found", 404)
    return send_file(cast(Path, current_app.config["RESUME_FOLDER"]).joinpath(filename))


############## tweet #######################


@visitor.route("/tweets/<tweet_id>")
def get_a_tweet(tweet_id: int):
    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        return abort("No tweet found", 404)
    return jsonify(get_tweet_detail(tweet)), 200


@visitor.route("/page-tweets/<int:page>")
def get_page_tweets(page: int):
    pagination = Tweet.query.order_by(Tweet.created_at.desc()).paginate(page=page, per_page=current_app.config["NUMBER_OF_PAGE_TWEETS"])  # type: ignore
    tweets = [get_tweet_detail(t) for t in pagination.items]
    return jsonify(tweets), 200


@visitor.route("/tweets")
def get_latest_tweet():
    tweet = Tweet.query.order_by(Tweet.created_at.desc()).first()  # type: ignore
    if not tweet:
        return abort("No tweet found", 404)
    return jsonify(get_tweet_detail(tweet)), 200  # type: ignore
