from datetime import datetime

from flask import jsonify


def abort(
    message: str = "error occured.",
    code: int = 400,
    target: str = "unknown",
):
    return (
        jsonify(dict(error=dict(message=message, code=code, target=target))),
        code,
    )


def serialize_datetime(date_object: datetime) -> str:
    return date_object.strftime("%Y-%m-%dT%H:%M:%S") + "+0000"
