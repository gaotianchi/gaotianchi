import click
from flask import Flask

from src.flaskextens import db


def register_commands(app: Flask) -> None:
    @app.cli.command("initdb", help="格式化数据库")
    def initdb():  # type: ignore
        # click.confirm(
        #     "该操作会格式化数据库，是否继续？",
        #     abort=True,
        # )
        db.drop_all()

        db.create_all()
        click.echo("完成数据格式化！")
