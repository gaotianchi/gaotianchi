from flask import Blueprint, g, jsonify, request

from src.database import User
from src.utlis import abort

from .apis import get_token_response_data, get_user_profile
from .auth import auth_required, generate_access_token

account = Blueprint("account", __name__)


@account.route("/users", methods=["POST"])
def post_a_user():
    user = User.create(request.json["username"], request.json["password"])  # type: ignore
    return jsonify(get_user_profile(user)), 201


@account.route("/token", methods=["POST"])
def post_token():
    current_user = User.query.filter_by(username=request.json["username"]).first()  # type: ignore
    if not current_user:
        return abort("No user found", 404, "username")
    if not current_user.validate_password(request.json["password"]):  # type: ignore
        return abort("Invalid password.", 401, "password")
    access_token = generate_access_token(current_user)  # type: ignore
    token_type = "Bearer"
    return jsonify(get_token_response_data(access_token, token_type)), 200


@account.route("/verify")
@auth_required
def verify_user():
    current_user = g.current_user
    if not current_user:
        return abort("No user found.", 401)
    return jsonify(get_user_profile(current_user)), 200


@account.route("/delete", methods=["DELETE"])
@auth_required
def delete_a_user():
    current_user = g.current_user
    if not current_user:
        return abort("No user found.", 401)
    current_user.delete()
    return "ok"
