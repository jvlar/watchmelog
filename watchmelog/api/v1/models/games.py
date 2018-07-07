from mongoengine import Document, IntField, StringField, BooleanField, ListField, ReferenceField
from typing import List

from watchmelog.api.v1.models.players import Player

MAP_CHOICES = [
    "Blizzard World",
    "Dorado",
    "Eichenwalde",
    "Hanamura",
    "Hollywood",
    "Horizon Lunar Colony",
    "Ilios",
    "Junkertown",
    "King's Row",
    "Lijiang Tower",
    "Nepal",
    "Numbani",
    "Oasis",
    "Rialto",
    "Route 66",
    "Temple of Anubis",
    "Volskaya Industry",
    "Watchpoint: Gibraltar"
]

HERO_CHOICES = [
    "Doomfist",
    "Junkrat",
    "Pharah",
    "Reaper",
    "McCree",
    "Solder: 76",
    "Widowmaker",
    "Genji",
    "Sombra",
    "Tracer",
    "Orisa",
    "Reinhardt",
    "Winston",
    "D.Va",
    "Roadhog",
    "Zarya",
    "Ana",
    "Brigitte",
    "Lucio",
    "Mercy",
    "Moira",
    "Zenyatta",
    "Bastion",
    "Hanzo",
    "Mei",
    "Symmetra",
    "Torbjorn"
]


class Game(Document):
    player: Player = ReferenceField(Player)
    season: int = IntField(min_value=1, max_value=11)
    sr: int = IntField(required=True, min_value=0, max_value=5000)
    map: str = StringField(choices=MAP_CHOICES)
    heroes: List[str] = ListField(field=StringField(choices=HERO_CHOICES))
    comment: str = StringField()
    thrower_team: bool = BooleanField(default=False)
    thrower_enemy_team: bool = BooleanField(default=False)
    leaver_team: bool = BooleanField(default=False)
    leaver_enemy_team: bool = BooleanField(default=False)
    group_with: List[str] = ListField(field=StringField())
