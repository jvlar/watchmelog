from apistar import App
from requests_oauthlib import OAuth2Session
from werkzeug.exceptions import abort

from watchmelog.config import app_config


_REGIONS = ["us", "eu", "apac"]

_BASE_AUTHORIZE_URI = "https://{region}.battle.net/oauth/authorize"
_BASE_TOKEN_URI = "https://{region}.battle.net/oauth/token"


def index(app: App):
    return app.render_template("index.jinja2")


def oauth_redirect(app: App, region: str):
    if region not in _REGIONS:
        abort(401, "region not valid")

    auth_url = _BASE_AUTHORIZE_URI.format(region=region)

    blizzard = OAuth2Session(app_config.oauth.client_id)
