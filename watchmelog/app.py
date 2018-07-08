import os
import pkg_resources

from flask import Flask

from watchmelog import db
from watchmelog.config import app_config
from watchmelog.web import auth, root


def create_app():

    package_root = pkg_resources.resource_filename("watchmelog", "")
    template_dir = os.path.join(package_root, "templates")
    static_dir = os.path.join(package_root, "static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = os.environ.get("SECRET_KEY", app_config.secret_key)

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
    app.register_blueprint(auth.bp, url_prefix="/auth")

    db.db.init_app(app)

    return app


if __name__ == "__main__":
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = os.environ.get("API_PORT", 5000)
    debug = os.environ.get("API_DEBUG", True)

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    _app = create_app()

    from werkzeug.contrib.fixers import ProxyFix

    _app.wsgi_app = ProxyFix(_app.wsgi_app)

    _app.run(host, int(port), debug=debug)
