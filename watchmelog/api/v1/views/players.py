from apistar.exceptions import BadRequest
from mongoengine import NotUniqueError

from watchmelog.api.v1.models.players import Player


def register_player(player: Player.Type) -> Player.Type:
    """
    This is coming from the docstring :D
    """
    new_player = Player(**player)
    try:
        new_player.save()
    except NotUniqueError as exc:
        raise BadRequest(detail=f"A player with the battletag {player.battletag} already exists.")
    print(new_player)

    return Player.Type(new_player)
