from apistar import types, validators
from typing import List

from watchmelog.api.v1.models.games import MAP_CHOICES, HERO_CHOICES


class LogGame(types.Type):
    season: int = validators.Number(1, 11, description="Overwatch season from 1 to 11.")
    sr: int = validators.Number(
        0, 5000, description="You SR at the end of the game from 0 to 5000."
    )
    map: str = validators.String(
        enum=MAP_CHOICES,
        allow_null=True,
        description=f"Name of the map the game was played.",
    )
    heroes: List[str] = validators.Array(
        items=validators.String(enum=HERO_CHOICES),
        unique_items=True,
        allow_null=True,
        description=f"List of heroes name that you played for that game.",
    )
    comment: str = validators.String(
        allow_null=True, description="Free text field to leave a comment for that game."
    )
    thrower_team: bool = validators.Boolean(
        allow_null=True, description="If there was a thrower in your team."
    )
    thrower_enemy_team: bool = validators.Boolean(
        allow_null=True, description="If there was a thrower in the enemy team."
    )
    leaver_team: bool = validators.Boolean(
        allow_null=True, description="If there was a leaver on your team."
    )
    leaver_enemy_team: bool = validators.Boolean(
        allow_null=True, description="If there was a leaver on the enemy team."
    )
    group_with: List[str] = validators.Array(
        items=validators.String(),
        allow_null=True,
        unique_items=True,
        description="List of people of you grouped with for this game.",
    )
