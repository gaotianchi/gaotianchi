import time
from functools import wraps
from typing import Any, Callable, Tuple, Union

from cryptography.fernet import Fernet, InvalidToken
from flask import current_app, g, request

from src.database import User
from src.utlis import abort


def generate_access_token(user: User) -> str:
    f = Fernet(current_app.config["SECRET_KEY"])  # type: ignore
    data = bytes(f"{user.username}", encoding="utf-8")
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
        user = User.query.filter_by(username=username.decode("utf-8")).first()  # type: ignore
        if not user:
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
        g.current_user = user
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
