import os

from flask import Flask
from flask_mongoengine import MongoEngine

from watchmelog.site import root

db = MongoEngine()


def create_app():
    app = Flask(__name__)
    if "MONGO_DB_NAME" in os.environ:
        app.config["MONGODB_SETTINGS"] = {
            "db": os.environ["MONGO_DB_NAME"],
            "alias": "default",
            "host": os.environ.get("MONGO_HOST"),
            "port": int(os.environ.get("MONGO_PORT")),
            "username": os.environ.get("MONGO_USER"),
            "password": os.environ.get("MONGO_PASS"),
        }
    else:
        app.config["MONGODB_SETTINGS"] = {"db": "watchmelog"}

    app.register_blueprint(root.bp, url_prefix="/")

    return app


if __name__ == "__main__":
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = os.environ.get("API_PORT", 5000)
    debug = os.environ.get("API_DEBUG", True)
    if debug:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    _app = create_app()
    _app.run(host, int(port), debug=debug)
