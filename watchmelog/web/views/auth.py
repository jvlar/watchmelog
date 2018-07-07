from apistar import http
from requests_oauthlib import OAuth2Session
from werkzeug.exceptions import abort

from watchmelog.config import app_config
from watchmelog.web.models.state import SessionState
from watchmelog.web.utils import redirect


_REGIONS = ["us", "eu", "apac"]

_BASE_AUTHORIZE_URI = "https://{region}.battle.net/oauth/authorize"
_BASE_TOKEN_URI = "https://{region}.battle.net/oauth/token"


def oauth_login_redirect(region: http.QueryParam):
    if region not in _REGIONS:
        abort(401, f"Region must be one of {_REGIONS}")

    base_auth_url = _BASE_AUTHORIZE_URI.format(region=region)
    blizzard = OAuth2Session(
        app_config.oauth.client_id, redirect_uri=app_config.oauth.redirect_uri
    )
    auth_url, state = blizzard.authorization_url(base_auth_url)

    SessionState(state=state, region=region).save()

    return redirect(auth_url)


def registration_redirect(code: http.QueryParam, state: http.QueryParam):
    session_state: SessionState = SessionState.objects(state=state).first()
    blizzard = OAuth2Session(
        app_config.oauth.client_id,
        state=session_state.state,
        redirect_uri=app_config.oauth.redirect_uri,
    )
    token_url = _BASE_TOKEN_URI.format(region=session_state.region)

    token = blizzard.fetch_token(
        token_url,
        code=code,
        client_id=app_config.oauth.client_id,
        client_secret=app_config.oauth.client_secret,
    )
    session_state.delete()

    # Profile URL: GET https://us.api.battle.net/account/user?access_token=TOKEN
    # >>> {"battletag": ..., "id": ...}

    # Call Blizzard to get player info
    # Create player model

    return redirect("/profile")
