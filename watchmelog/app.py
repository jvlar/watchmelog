import os

from apistar import App, Include, Route, Component, http
from apistar_cors_hooks import CORSRequestHooks
from mongoengine import connect

from watchmelog import web, config
from watchmelog.api import v1
from watchmelog.api.v1.auth import AuthComponent


config.load_config()

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

if "MONGO_CONN_STR" in os.environ:
    connect(os.environ["MONGO_CONN_STR"])
else:
    connect("watchmelog")

routes = [
    Route("/", method="GET", handler=web.index),
    Include("/v1/players", name="v1 players", routes=v1.routes),
]

app = App(
    routes=routes,
    components=[AuthComponent()],
    event_hooks=[CORSRequestHooks()],
    template_dir=TEMPLATE_DIR,
)

if __name__ == "__main__":
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = os.environ.get("API_PORT", 5000)
    debug = os.environ.get("API_DEBUG", True)
    app.serve(host, int(port), debug=debug)
