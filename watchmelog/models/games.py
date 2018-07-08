from typing import List

from mongoengine import signals

from watchmelog.db import db
from watchmelog.models.players import Player, PLATFORM_CHOICES, REGION_CHOICES
from watchmelog.template_helpers import get_curr_season
from watchmelog.utils import update_timestamp, utcnow

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
    "Volskaya Industries",
    "Watchpoint: Gibraltar",
]

HERO_CHOICES = [
    "Doomfist",
    "Junkrat",
    "Pharah",
    "Reaper",
    "McCree",
    "Soldier: 76",
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
    "Torbjorn",
]

RESULT_CHOICES = ["win", "loss", "draw"]


class Game(db.Document):
    player: Player = db.ReferenceField(Player)
    season: int = db.IntField(min_value=1, max_value=get_curr_season())
    sr: int = db.IntField(min_value=0, max_value=5000)
    result: str = db.StringField(choices=RESULT_CHOICES)
    placement: bool = db.BooleanField(default=False)
    map: str = db.StringField(choices=MAP_CHOICES)
    heroes: List[str] = db.ListField(field=db.StringField(choices=HERO_CHOICES))
    comment: str = db.StringField()
    thrower_team: bool = db.BooleanField(default=False)
    thrower_enemy_team: bool = db.BooleanField(default=False)
    leaver_team: bool = db.BooleanField(default=False)
    leaver_enemy_team: bool = db.BooleanField(default=False)
    group_with: List[str] = db.ListField(field=db.StringField())
    platform = db.StringField(required=True, choices=PLATFORM_CHOICES)
    region = db.StringField(required=True, choices=REGION_CHOICES)
    created_at = db.DateTimeField(default=utcnow)
    updated_at = db.DateTimeField()


signals.pre_save.connect(update_timestamp, sender=Game)
