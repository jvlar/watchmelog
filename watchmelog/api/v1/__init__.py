from apistar import Route

from watchmelog.api.v1.views.players import (
    register_player,
    generate_api_key,
    get_player,
)

routes = [
    Route("/{player_slug}", "GET", get_player, name="Get Player's information"),
    Route("", "POST", register_player, name="Register Player"),
    Route(
        "/{player_slug}/apikey", "POST", generate_api_key, name="Generate new API Key"
    ),
]
