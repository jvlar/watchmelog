from apistar import Route

from watchmelog.web.views import auth

routes = [
    Route("/login", method="GET", handler=auth.oauth_login_redirect),
    Route("/registration", method="GET", handler=auth.registration_redirect),
]
