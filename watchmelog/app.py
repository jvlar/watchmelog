import os

from apistar import App, Include
from apistar_cors_hooks import CORSRequestHooks
from mongoengine import connect

from watchmelog.api import v1
from watchmelog.api.v1.auth import AuthComponent

if "MONGO_CONN_STR" in os.environ:
    connect(os.environ["MONGO_CONN_STR"])
else:
    connect("watchmelog")

routes = [Include("/v1/players", name="v1 players", routes=v1.routes)]

app = App(routes=routes, components=[AuthComponent()], event_hooks=[CORSRequestHooks()])

if __name__ == "__main__":
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = os.environ.get("API_PORT", 5000)
    debug = os.environ.get("API_DEBUG", True)
    app.serve(host, int(port), debug=debug)
