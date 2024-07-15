from flask import Blueprint

from .account import account
from .author import author
from .visitor import visitor

v1 = Blueprint("v1", __name__)
v1.register_blueprint(account)
v1.register_blueprint(author)
v1.register_blueprint(visitor)


@v1.route("/v1")
def v1_hello():
    return "v1"
