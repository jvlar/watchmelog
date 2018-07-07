import bcrypt
from apistar import Route, http
from apistar.exceptions import BadRequest, NotFound, Forbidden
from typing import List

from watchmelog.utils import hash_pass, mongo_to_dict
from watchmelog.api.v1.models.games import Game
from watchmelog.api.v1.models.players import Player, ApiKey
from watchmelog.api.v1.types.games import LogGame
from watchmelog.api.v1.types.players import RegisterPlayer, Login


def get_player(player_slug: str, auth_player: Player) -> dict:
    return mongo_to_dict(auth_player)


def register_player(player: RegisterPlayer) -> dict:
    """
    Register a new Overwatch player.
    """
    player.password = hash_pass(player.password.encode("utf-8"))
    if Player.objects(battletag=player.battletag):
        raise BadRequest(
            detail=f"A player with the battletag {player.battletag} already exists."
        )

    new_player = Player(**player)
    new_player.save()

    return mongo_to_dict(new_player)


def generate_api_key(player_slug: str, login_payload: Login) -> dict:
    """
    Generate a new API Key for the player.
    If an old key already exist, it will be deleted.
    """
    player = Player.objects(slug=player_slug).first()
    if not player:
        raise NotFound(f"Player {player_slug} not found.")

    if (
        not bcrypt.hashpw(
            login_payload.password.encode("utf-8"), player.password.encode("utf-8")
        ).decode("utf-8")
        == player.password
    ):
        raise Forbidden("Wrong password")

    old_api_key = ApiKey.objects(player=player)
    if old_api_key:
        for key in old_api_key:
            key.delete()

    new_api_key = ApiKey(player=player)
    new_api_key.save()
    return mongo_to_dict(new_api_key)


def log_game(
    auth_player: Player,
    player_slug: str,
    platform: str,
    region: str,
    new_game_payload: LogGame,
) -> dict:
    """
    Log a new game in the system.
    """
    new_game = Game(
        **{
            **new_game_payload,
            **{"platform": platform, "region": region, "player": player_slug},
        }
    )
    new_game.save()
    return mongo_to_dict(new_game)


def list_player_games(
    auth_player: Player, player_slug: str, filters: http.QueryParams
) -> List[dict]:

    dict_filters = dict(filters)

    if dict_filters.get("player", player_slug) != player_slug:
        raise Forbidden(
            f"Cannot list games filtered on player {dict_filters['player']}"
        )

    order = dict_filters.pop("order", "asc")
    order_by = dict_filters.pop("order_by", "created_at")

    games = (
        Game.objects(**dict_filters)
        .order_by(f"{'-' if order == 'desc' else ''}{order_by}")
        .all()
    )
    return [mongo_to_dict(g) for g in games]


routes = [
    Route("/{player_slug}", "GET", get_player, name="Get Player's information"),
    Route("", "POST", register_player, name="Register Player"),
    Route(
        "/{player_slug}/apikey", "POST", generate_api_key, name="Generate new API Key"
    ),
    Route(
        "/{player_slug}/{platform}/{region}/games",
        "POST",
        log_game,
        name="Log a new game",
    ),
    Route(
        "/{player_slug}/games",
        "GET",
        list_player_games,
        name="List all games for player.",
    ),
]
