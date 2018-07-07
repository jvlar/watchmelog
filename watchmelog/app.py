from apistar import App, Include
from apistar_cors_hooks import CORSRequestHooks
from mongoengine import connect

from watchmelog.api import v1
from watchmelog.api.v1.auth import AuthComponent

connect("watchmelog")

routes = [Include("/v1/players", name="v1 players", routes=v1.routes)]

app = App(routes=routes, components=[AuthComponent()], event_hooks=[CORSRequestHooks()])

if __name__ == "__main__":
    app.serve("127.0.0.1", 5000, debug=True)
