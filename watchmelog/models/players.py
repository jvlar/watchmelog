import secrets
from mongoengine import (
    StringField,
    DateTimeField,
    ReferenceField,
    IntField,
    BooleanField,
)
from slugify import slugify

from watchmelog.db import db
from watchmelog.utils import utcnow

PLATFORM_CHOICES = ["pc", "xbox", "ps4"]
REGION_CHOICES = ["us", "eu", "apac"]


class Player(db.Document):
    slug = StringField(primary_key=True)
    battletag = StringField(required=True, unique=True)
    blizzard_id = IntField(required=True)
    default_platform = StringField(choices=PLATFORM_CHOICES)
    default_region = StringField(required=True, choices=REGION_CHOICES)
    created_at = DateTimeField(default=utcnow)

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.slug = slugify(self.battletag)


class ApiKey(db.Document):
    _black_list = ["id"]

    player: Player = ReferenceField(Player)
    key: str = StringField(required=True, default=secrets.token_urlsafe(32))
    created_at = DateTimeField(required=True, default=utcnow)
    valid = BooleanField(required=True, default=True)
