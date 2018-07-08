from apistar import Component, http
from apistar.exceptions import BadRequest, Forbidden

from watchmelog.api.v1.models.players import Player, ApiKey


class AuthComponent(Component):
    def resolve(self, x_api_key: http.Header, player_slug: str = None) -> Player:
        if not x_api_key:
            raise BadRequest("Missing header x-old-api-key.")

        api_key: ApiKey = ApiKey.objects(key=x_api_key)
        if not api_key:
            raise BadRequest("Could not find a valid Api Key.")
        api_key = api_key[0]

        if player_slug and player_slug != api_key.player.slug:
            raise Forbidden("You cannot access that player.")

        return api_key.player
