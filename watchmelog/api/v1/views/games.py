from apistar import Route
from apistar.exceptions import NotFound

from watchmelog.api.utils import mongo_to_dict
from watchmelog.api.v1.models.games import Game
from watchmelog.api.v1.models.players import Player
from watchmelog.api.v1.types.games import LogGame


def log_game(new_game_payload: LogGame) -> dict:
    player = Player.objects(slug=new_game_payload.player_slug)
    if not player:
        raise NotFound(f"Could not find player {new_game_payload.player_slug}.")

    new_game_dict = dict(new_game_payload)
    new_game_dict["player"] = player[0]
    new_game_dict.pop("player_slug")
    new_game = Game(**new_game_dict)
    new_game.save()
    return mongo_to_dict(new_game)


routes = [Route("", "POST", log_game, name="Log a new game")]
