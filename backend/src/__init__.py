from flask import Flask

from .commands import register_commands
from .flaskextens import cors, db
from .settings import get_config


def create_app() -> Flask:
    config = get_config()
    app = Flask("twitter")
    app.config.from_object(config)
    db.init_app(app)
    cors.init_app(app)
    register_commands(app)
    match config.VERSION:  # type: ignore
        case "1":
            from .apis.v1 import v1

            app.register_blueprint(v1)
        case "2":
            from .apis.v2 import v2

            app.register_blueprint(v2)

    return app
