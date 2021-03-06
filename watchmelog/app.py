import os
import pkg_resources

from flask import Flask

from watchmelog import db
from watchmelog.config import app_config
from watchmelog import template_helpers
from watchmelog.web import auth, root, csv, games

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
app.register_blueprint(games.bp, url_prefix="/games")
app.register_blueprint(csv.bp, url_prefix="/csv")

app.jinja_env.globals.update(
    get_curr_season=template_helpers.get_curr_season,
    form_status_class=template_helpers.form_status_class,
)

app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

db.db.init_app(app)


if __name__ == "__main__":
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = os.environ.get("API_PORT", 5000)
    debug = os.environ.get("API_DEBUG", True)

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    from werkzeug.contrib.fixers import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.run(host, int(port), debug=debug)
