from apistar import Route

from watchmelog.web.views import auth, web

routes = [
    Route("", method="GET", handler=web.index),
    Route("profile", method="GET", handler=web.profile),
    Route("login", method="GET", handler=auth.oauth_login_redirect),
    Route("registration", method="GET", handler=auth.registration_redirect),
]
