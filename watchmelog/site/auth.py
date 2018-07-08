from flask import Blueprint, request, abort, redirect, url_for, session
from requests_oauthlib import OAuth2Session

from watchmelog.config import app_config
from watchmelog.core.player import create_or_update_player, ensure_api_key_for_player
from watchmelog.models.state import SessionState


bp = Blueprint("auth", __name__)

_REGIONS = ["us", "eu", "apac"]

_BASE_AUTHORIZE_URI = "https://{region}.battle.net/oauth/authorize"
_BASE_TOKEN_URI = "https://{region}.battle.net/oauth/token"


@bp.route("/login")
def oauth_login_redirect():
    """
    Redirects a user to the specified Blizzard OAuth login page.
    """
    region = request.args.get("region", "").lower()

    if region not in _REGIONS:
        abort(400, f"Region must be one of {_REGIONS}")

    base_auth_url = _BASE_AUTHORIZE_URI.format(region=region)
    blizzard = OAuth2Session(
        app_config.oauth.client_id, redirect_uri=app_config.oauth.redirect_uri
    )
    auth_url, state = blizzard.authorization_url(base_auth_url)

    SessionState(state=state, region=region).save()

    return redirect(auth_url)


@bp.route("/register")
def oauth_registration_redirect():
    """
    Receives a code from Blizzard's OAuth login page after it has been
    filled by the user.
    """
    code = request.args["code"]
    state = request.args["state"]

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
    player = create_or_update_player(token, session_state.region)
    api_key = ensure_api_key_for_player(player)

    session["api_key"] = api_key.key

    session_state.delete()

    return redirect(url_for("root.root"))
