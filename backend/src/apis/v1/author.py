from pathlib import Path
from typing import cast

from flask import Blueprint, current_app, g, jsonify, request

from src.apis.v1.database import Photo, Resume, Tweet
from src.utlis import abort

from .apis import *
from .auth import auth_required

author = Blueprint("author", __name__)


################# resume ########################


@author.route("/resume", methods=["PUT"])
@auth_required
def put_a_resume():
    file = request.files.get("resume")
    if not file:
        return abort("No resume found.", 404)
    old_resume = cast(Path, current_app.config["RESUME_FOLDER"]).joinpath(
        g.current_user.resume.filename
    )
    if old_resume.exists():
        old_resume.unlink()
    filename = g.current_user.username + "-" + cast(str, file.filename)
    resume_path = cast(Path, current_app.config["RESUME_FOLDER"]).joinpath(filename)
    file.save(resume_path)
    resume = Resume.create(filename, g.current_user.id)
    return jsonify(get_resume_profile(resume)), 200


############################## photo #####################################


@author.route("/photos", methods=["POST"])
@auth_required
def post_a_photo():
    current_user = g.current_user
    file = request.files.get("file")
    file.save(current_app.config["UPLOAD_FOLDER"].joinpath(file.filename))  # type: ignore
    photo = Photo.create(file.filename, request.form.get("tweetId"), current_user.id)  # type: ignore
    return jsonify(get_photo_detail(photo)), 201


############################ tweet ###############################


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


################ user ########################


@author.route("/user-profile/<username>", methods=["PATCH"])
@auth_required
def patch_a_userprofile(username: str):
    user = User.query.filter_by(username=username).first()  # type: ignore
    user.update_profile(request.json["profile"])  # type: ignore
    return jsonify(get_user_profile(user)), 200  # type: ignore
