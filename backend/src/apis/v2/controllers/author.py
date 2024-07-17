import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Tuple, Union, cast

from cryptography.fernet import Fernet, InvalidToken
from flask import Blueprint, current_app, g, jsonify, request

from src.apis.v2.database import Me
from src.apis.v2.serializer import *
from src.utlis import abort

author = Blueprint("author", __name__)


##################### auth ##########################
def generate_access_token(me: Me) -> str:
    f = Fernet(current_app.config["SECRET_KEY"])  # type: ignore
    data = bytes(f"{me.username}", encoding="utf-8")
    return f.encrypt(data).decode("utf-8")


def get_access_token():
    if "Authorization" in request.headers:
        try:
            token_type, access_token = request.headers["Authorization"].split(None, 1)
        except ValueError:
            token_type = access_token = None
    else:
        token_type = access_token = None

    return token_type, access_token


def validate_access_token(token: str) -> bool:
    f = Fernet(current_app.config["SECRET_KEY"])  # type: ignore
    try:
        username = f.decrypt(token.encode("utf-8"))
        if not username:
            return False
        me = Me.query.filter_by(username=username.decode("utf-8")).first()  # type: ignore
        if not me:
            return False
        else:
            f.decrypt_at_time(
                token.encode("utf-8"),
                604800,
                int(time.time()),
            )
    except InvalidToken:
        return False
    except Exception:
        return False
    else:
        g.me = me
        return True


def auth_required(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)  # type: ignore
    def decorated(
        *args: Any, **kwargs: Any
    ) -> Union[Callable[..., Any], Tuple[Any, int]]:
        token_type, access_token = get_access_token()

        if request.method != "OPTIONS":
            if token_type is None or token_type.lower() != "bearer":
                return abort("The token type must be bearer.")
            if access_token is None:
                return abort("No access token found.")
            if not validate_access_token(access_token):
                return abort("Invalid token.", 401)
        return f(*args, **kwargs)

    return decorated


@author.route("/token", methods=["POST"])
def post_token():
    current_user = Me.query.filter_by(username=request.json["username"]).first()  # type: ignore
    if not current_user:
        return abort("No user found", 404, "username")
    if not current_user.validate_password(request.json["password"]):  # type: ignore
        return abort("Invalid password.", 401, "password")
    access_token = generate_access_token(current_user)  # type: ignore
    token_type = "Bearer"
    return jsonify(get_token_response_data(access_token, token_type)), 200


@author.route("/verify")
@auth_required
def verify_user():
    return jsonify(get_my_profile(g.me)), 200


########################## user restful ##########################
@author.route("/me", methods=["POST"])
def post_me():
    me = Me.post_me(request.json["username"], request.json["password"])  # type: ignore
    return jsonify(get_my_profile(me)), 201


@author.route("/resume", methods=["PUT"])
@auth_required
def put_a_resume():
    resume = request.files.get("resume")
    if not resume:
        return abort("No resume uploaded.", 404)
    resume_path = cast(Path, current_app.config["RESUME_PATH"])
    if resume_path.exists():
        resume_path.unlink()
    resume.save(resume_path)  # type: ignore
    return (
        jsonify({"resumeUrl": url_for("v2.visitor.get_resume_url", _external=True)}),
        201,
    )


@author.route("/me", methods=["PATCH"])
@auth_required
def patch_me():
    me = g.me.patch_me(
        author_name=request.json["authorName"],  # type: ignore
        profile=request.json["profile"],  # type: ignore
        blog_title=request.json["blogTitle"],  # type: ignore
        blog_sub_title=request.json["blogSubTitle"],  # type: ignore
        resume=request.json["resume"],  # type: ignore
    )
    return jsonify(get_my_detail(me)), 200


###################### tweet restful ##############################
@author.route("/tweets", methods=["POST"])
@auth_required
def post_a_tweet():
    t = Tweet.post_tweet(request.json["text"], g.me.id)  # type: ignore
    return jsonify(get_tweet_profile(t)), 201


@author.route("/tweets/<tweet_id>", methods=["PATCH"])
@auth_required
def patch_a_tweet(tweet_id: int):
    t = Tweet.query.get(tweet_id)
    if not t:
        return abort(code=404)
    t = t.patch_tweet(request.json["text"])  # type: ignore
    return jsonify(get_tweet_detail(t)), 200


@author.route("/tweets/<tweet_id>", methods=["DELETE"])
@auth_required
def delete_a_tweet(tweet_id: int):
    t = Tweet.query.get(tweet_id)
    for p in t.photos:  # type: ignore
        p_path = current_app.config["PHOTO_FOLDER"].joinpath(p.filename)
        p_path.unlink()
    if not t:
        return abort(code=404)
    t.delete()
    return jsonify({"ok": "ok"})


########################### photo ####################################
@author.route("/photos", methods=["POST"])
@auth_required
def post_a_photo():
    file = request.files.get("photo")
    if not file:
        return abort("No photo found", 404)
    photo_path = current_app.config["PHOTO_FOLDER"].joinpath(file.filename)
    file.save(photo_path)
    p = Photo.post_me(file.filename, request.form.get("tweetId"), g.me.id)  # type: ignore
    return jsonify(get_photo_detail(p)), 201
