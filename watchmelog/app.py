from apistar import App
from mongoengine import connect

from watchmelog.api import v1

connect("watchmelog")

routes = v1.routes

app = App(routes=routes)

if __name__ == "__main__":
    app.serve("127.0.0.1", 5000, debug=True)
