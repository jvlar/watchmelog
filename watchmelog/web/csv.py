from flask import Blueprint, render_template, request

from watchmelog.web.utils import needs_auth

bp = Blueprint("csv", __name__)


@bp.route("/import", methods=["GET", "POST"])
@needs_auth
def import_csv():
    if request.method == "POST":
        print(request.form)
    return render_template("player/csv_import.jinja2")
