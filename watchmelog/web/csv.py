from flask import Blueprint, render_template, request
import csv
import io

from watchmelog.config import app_config
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

            season = request.form["season"]
            matches = csv.DictReader(
                io.StringIO(request.files["csv_file"].stream.read().decode("utf-8"))
            )
        except ValueError:
            return render_template("player/csv_import.jinja2", **ctx)

    return render_template("player/csv_import.jinja2")
