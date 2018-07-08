from flask import Blueprint, render_template, request, session, redirect, url_for

from watchmelog.config import app_config
from watchmelog.core.csv import import_raw_csv
from watchmelog.core.player import get_player_from_api_key
from watchmelog.web.utils import needs_auth, allowed_file

bp = Blueprint("csv", __name__)


@bp.route("/import", methods=["GET", "POST"])
@needs_auth
def import_csv():
    ctx = {"errors": []}
    if request.method == "POST":
        # Validate form
        try:
            if "season" not in request.form:
                ctx["errors"].append("Season not provided")
                raise ValueError

            try:
                int(request.form["season"])
            except ValueError:
                ctx["errors"].append("Season is not a valid number")
                raise ValueError

            if (
                int(request.form["season"]) < 1
                or int(request.form["season"]) > app_config.current_season
            ):
                ctx["errors"].append("Invalid season value")
                raise ValueError

            if "csv_file" not in request.files:
                ctx["errors"].append("No CSV file provided")
                raise ValueError

            filename = request.files["csv_file"].filename
            if not allowed_file(filename, ["csv"]):
                ctx["errors"].append("File extension must be '.csv'")
                raise ValueError

            player = get_player_from_api_key(session["api_key"])
            season = request.form["season"]
            raw_matches = request.files["csv_file"].stream.read().decode("utf-8")

            success, errors = import_raw_csv(player, season, raw_matches)
            if not success:
                ctx["errors"] = errors
                raise ValueError
            return redirect(url_for("root.root"))
        except ValueError:
            return render_template("player/csv_import.jinja2", **ctx)

    return render_template("player/csv_import.jinja2")
