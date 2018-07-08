from flask import Blueprint, session, render_template

from watchmelog.core.player import get_player_from_api_key

bp = Blueprint("root", __name__)


@bp.route("/")
def root():
    ctx = {}

    player = get_player_from_api_key(session.get("api_key"))
    if player:
        ctx["battletag"] = player.battletag

    return render_template("index.jinja2", **ctx)
