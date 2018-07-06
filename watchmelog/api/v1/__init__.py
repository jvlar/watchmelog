from apistar import Route

from watchmelog.api.v1.views.players import register_player

routes = [Route('/v1/players', 'POST', register_player, name='Register Player')]