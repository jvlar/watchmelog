import secrets
from mongoengine import Document, StringField, DateTimeField, ReferenceField
from slugify import slugify

from watchmelog.api.utils import utcnow

PLATFORM_CHOICES = ["PC", "XBOX", "PS4"]
REGION_CHOICES = ["US", "EU", "ASIA"]


class Player(Document):
    _black_list = ["password"]

    battletag = StringField(required=True, unique=True)
    password = StringField(required=True)
    platform = StringField(required=True, choices=PLATFORM_CHOICES)
    region = StringField(required=True, choices=REGION_CHOICES)
    slug = StringField(primary_key=True)
    created_at = DateTimeField(default=utcnow)

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.slug = slugify(self.battletag)


class ApiKey(Document):
    _black_list = ["id"]

    player: Player = ReferenceField(Player)
    key: str = StringField(default=secrets.token_urlsafe(32))
