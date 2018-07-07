from mongoengine import Document, StringField, DateTimeField

from watchmelog import utils


class SessionState(Document):
    state = StringField(primary_key=True)
    region = StringField(required=True)
    created = DateTimeField(default=utils.utcnow, required=True)

    meta = {"indexes": [{"fields": ["created"], "expireAfterSeconds": 300}]}
