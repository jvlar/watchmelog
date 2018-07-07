import os

from apistar import App, Include
from apistar_cors_hooks import CORSRequestHooks
from mongoengine import connect

from watchmelog import web
from watchmelog.api.v1.auth import AuthComponent
from watchmelog.api.v1.views import players as v1_players


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

if "MONGO_CONN_STR" in os.environ:
    connect(host=os.environ["MONGO_CONN_STR"])
else:
    connect("watchmelog")

routes = [
    Include("/", name="web", routes=web.routes, documented=False),
    Include("/v1/players", name="v1 Player", routes=v1_players.routes),
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
    if debug:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.serve(host, int(port), debug=debug)
