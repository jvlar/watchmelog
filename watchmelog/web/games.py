from flask import Blueprint, request, flash, redirect, url_for, render_template

from watchmelog.forms import GameForm

bp = Blueprint("game", __name__)


@bp.route("/log", methods=["GET", "POST"])
def log_game():
    form = GameForm()
    if request.method == "POST" and form.validate():
        flash("Game logged!")
        return redirect(url_for("root.root"))
    print("piss")
    for field in form:
        print(type(field))
        print(field.errors)

    return render_template("log_game.jinja2", form=form)
