import bcrypt
from mongoengine import (
    Document,
    DateTimeField,
    StringField,
    FloatField,
    IntField,
    ListField,
    EmbeddedDocumentField,
    ObjectIdField,
)
from typing import List


def hash_pass(password: bytes, salt: str = None) -> str:
    hashed_password: bytes = bcrypt.hashpw(password, salt or bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def mongo_to_dict(obj, black_list: List = None):
    """
    Turn a mongoengine object into a jsonible python object
    """

    if not black_list:
        black_list = getattr(obj, "_black_list", [])

    return_data = []

    if isinstance(obj, Document) and not "id" in black_list:
        return_data.append(("id", str(obj.id)))

    for field_name in obj._fields:
        if field_name in black_list:
            continue
        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], DateTimeField):
            return_data.append((field_name, str(data.isoformat())))

        elif isinstance(obj._fields[field_name], StringField):
            return_data.append((field_name, str(data)))

        elif isinstance(obj._fields[field_name], FloatField):
            return_data.append((field_name, float(data)))

        elif isinstance(obj._fields[field_name], IntField):
            return_data.append((field_name, int(data)))

        elif isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, data))

        elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data)))

        elif isinstance(obj._fields[field_name], ObjectIdField):
            return_data.append((field_name, str(data)))

    return dict(return_data)
