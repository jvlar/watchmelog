import bcrypt
from apistar import Route
from apistar.exceptions import BadRequest, NotFound, Forbidden

from watchmelog.utils import hash_pass, mongo_to_dict
from watchmelog.api.v1.models.players import Player, ApiKey
from watchmelog.api.v1.types.players import RegisterPlayer, Login


def get_player(player_slug: str, auth_player: Player) -> dict:
    if auth_player.slug != player_slug:
        raise Forbidden("You cannot access that player.")
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
    try:
        player = Player.objects(slug=player_slug)[0]
    except IndexError:
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


routes = [
    Route("/{player_slug}", "GET", get_player, name="Get Player's information"),
    Route("", "POST", register_player, name="Register Player"),
    Route(
        "/{player_slug}/apikey", "POST", generate_api_key, name="Generate new API Key"
    ),
]
