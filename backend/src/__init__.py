from flask import Flask

from .apis import v1_bp
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
    app.register_blueprint(v1_bp)

    @app.route("/")
    def hello():  # type: ignore
        return "hello"

    return app
