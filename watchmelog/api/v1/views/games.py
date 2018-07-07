from apistar import Route

from watchmelog.utils import mongo_to_dict
from watchmelog.api.v1.models.games import Game
from watchmelog.api.v1.types.games import LogGame


def log_game(new_game_payload: LogGame) -> dict:
    new_game = Game(**new_game_payload)
    new_game.save()
    return mongo_to_dict(new_game)


routes = [Route("", "POST", log_game, name="Log a new game")]
