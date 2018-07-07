from apistar import types, validators
from apistar.exceptions import BadRequest, NotFound
from mongoengine import NotUniqueError

from watchmelog.api.utils import hash_pass, mongo_to_dict
from watchmelog.api.v1.models.players import Player, ApiKey


class RegisterPlayer(types.Type):
    battletag: str = validators.String(description="Your Battle.net Tag")
    password: str = validators.String(
        min_length=12, description="Password used to authenticate with the API."
    )
    platform: str = validators.String(
        enum=["PC", "XBOX", "PS4"], description="Platform you're playing on."
    )
    region: str = validators.String(
        enum=["US", "EU", "ASIA"], description="Region you're playing on."
    )


def register_player(player: RegisterPlayer) -> dict:
    """
    Register a new Overwatch player.
    """
    player.password = hash_pass(player.password.encode("utf-8"))
    new_player = Player(**player)
    try:
        new_player.save()
    except NotUniqueError:
        raise BadRequest(
            detail=f"A player with the battletag {player.battletag} already exists."
        )

    return mongo_to_dict(new_player, black_list=["password"])


def generate_api_key(player_slug: str) -> dict:
    try:
        player = Player.objects(slug=player_slug)[0]
    except IndexError:
        raise NotFound(f"Player {player_slug} not found.")

    old_api_key = ApiKey.objects(player=player)
    if old_api_key:
        for key in old_api_key:
            key.delete()
    new_api_key = ApiKey(player=player)
    new_api_key.save()
    return mongo_to_dict(new_api_key)
