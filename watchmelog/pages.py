from apistar import App


def index(app: App):
    return app.render_template("index.jinja2")
