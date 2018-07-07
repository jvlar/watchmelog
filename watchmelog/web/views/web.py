from apistar import App, http


def index(app: App):
    return app.render_template("index.jinja2")


def profile(app: App):
    return app.render_template("profile.jinja2")
