from flask import Blueprint

from .controllers import author, visitor

v2 = Blueprint("v2", __name__)

v2.register_blueprint(author)
v2.register_blueprint(visitor)
