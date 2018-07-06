import pendulum as pendulum
from apistar import types, validators
from mongoengine import Document, StringField, DateTimeField
from slugify import slugify


class Player(Document):
    battletag = StringField(required=True, max_length=50, unique=True)
    platform = StringField(required=True)
    region = StringField(required=True)
    slug = StringField()
    created_at = DateTimeField(default=pendulum.now('UTC'))

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.slug = slugify(self.battletag)


    class Type(types.Type):
        battletag = validators.String(max_length=50, description="Your Battle.net Tag")
        platform = validators.String(
            enum=["PC", "XBOX", "PS4"], description="Platform you're playing on."
        )
        region = validators.String(
            enum=["US", "EU", "ASIA"], description="Region you're playing on."
        )
