from apistar import types, validators
from typing import List

from watchmelog.api.v1.models.games import MAP_CHOICES, HERO_CHOICES


class LogGame(types.Type):
    player_slug: str = validators.String()
    season: int = validators.Number(1, 11)
    sr: int = validators.Number(0, 5000)
    map: str = validators.String(enum=MAP_CHOICES, allow_null=True)
    heroes: List[str] = validators.Array(
        items=validators.String(enum=HERO_CHOICES), unique_items=True, allow_null=True
    )
    comment: str = validators.String(allow_null=True)
    thrower_team: bool = validators.Boolean(allow_null=True)
    thrower_enemy_team: bool = validators.Boolean(allow_null=True)
    leaver_team: bool = validators.Boolean(allow_null=True)
    leaver_enemy_team: bool = validators.Boolean(allow_null=True)
    group_with: List[str] = validators.Array(
        items=validators.String(), allow_null=True, unique_items=True
    )
