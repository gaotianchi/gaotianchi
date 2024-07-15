from flask import Blueprint, current_app, g, jsonify, request

from src.database import Photo, Tweet
from src.utlis import abort

from .apis import *
from .auth import auth_required

author = Blueprint("author", __name__)


@author.route("/photos", methods=["POST"])
@auth_required
def post_a_photo():
    current_user = g.current_user
    file = request.files.get("file")
    file.save(current_app.config["UPLOAD_FOLDER"].joinpath(file.filename))  # type: ignore
    photo = Photo.create(file.filename, request.form.get("tweetId"), current_user.id)  # type: ignore
    return jsonify(get_photo_detail(photo)), 201


@author.route("/tweets", methods=["POST", "PATCH"])
@auth_required
def post_a_tweet():
    current_user = g.current_user
    tweet = Tweet.create(request.json["text"], current_user.id)  # type: ignore
    return jsonify(get_tweet_profile(tweet)), 201


@author.route("/tweets/<tweet_id>", methods=["DELETE"])
@auth_required
def delete_a_tweet(tweet_id: int):
    tweet = Tweet.query.get(tweet_id)
    tweet.delete()  # type: ignore
    return jsonify("ok"), 204


@author.route("/tweets/<tweet_id>", methods=["PATCH"])
@auth_required
def patch_a_tweet(tweet_id: int):
    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        return abort("No tweet found", 404)
    tweet.update(request.json["text"])  # type: ignore
    return jsonify(get_tweet_detail(tweet)), 200


@author.route("/user-profile/<username>", methods=["PATCH"])
@auth_required
def patch_a_userprofile(username: str):
    user = User.query.filter_by(username=username).first()  # type: ignore
    user.update_profile(request.json["profile"])  # type: ignore
    return jsonify(get_user_profile(user)), 200  # type: ignore


@author.route("/resume", methods=["POST"])
@auth_required
def update_user_resume():
    original_resume = current_app.config["UPLOAD_FOLDER"].parent.joinpath("resume.pdf")  # type: ignore
    if original_resume.exists():  # type: ignore
        original_resume.unlink()  # type: ignore
    file = request.files.get("file")
    file.save(current_app.config["UPLOAD_FOLDER"].parent.joinpath("resume.pdf"))  # type: ignore
    url = url_for("v1.visitor.get_resume", _external=True)
    return jsonify(dict(url=url)), 200
