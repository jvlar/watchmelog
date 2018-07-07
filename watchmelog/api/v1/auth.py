from apistar import Component, http
from apistar.exceptions import BadRequest

from watchmelog.api.v1.models.players import Player, ApiKey


class AuthComponent(Component):
    def resolve(self, x_api_key: http.Header) -> Player:
        if not x_api_key:
            raise BadRequest("Missing header x-api-key.")

        api_key: ApiKey = ApiKey.objects(key=x_api_key)
        if not api_key:
            raise BadRequest("Could not find a valid Api Key.")
        api_key = api_key[0]

        return api_key.player
