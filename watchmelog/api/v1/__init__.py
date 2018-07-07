from apistar import Route

from watchmelog.api.v1.views.players import register_player, generate_api_key

routes = [
    Route("/v1/players", "POST", register_player, name="Register Player"),
    Route(
        "/v1/players/{player_slug}/apikey",
        "GET",
        generate_api_key,
        name="Generate new API Key",
    ),
]
