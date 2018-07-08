from mongoengine import StringField, DateTimeField

from watchmelog import utils
from watchmelog.db import db


class SessionState(db.Document):
    state = StringField(primary_key=True)
    region = StringField(required=True)
    created = DateTimeField(default=utils.utcnow, required=True)

    meta = {"indexes": [{"fields": ["created"], "expireAfterSeconds": 300}]}
