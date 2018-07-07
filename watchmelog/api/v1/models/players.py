import pendulum as pendulum
from mongoengine import Document, StringField, DateTimeField
from slugify import slugify


class Player(Document):
    battletag = StringField(required=True, unique=True)
    password = StringField(required=True)
    platform = StringField(required=True)
    region = StringField(required=True)
    slug = StringField()
    created_at = DateTimeField(default=pendulum.now("UTC"))

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.slug = slugify(self.battletag)
