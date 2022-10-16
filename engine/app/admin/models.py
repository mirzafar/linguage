from mongoengine import *


class User(Document):
    name = StringField(required=True)
    last_name = StringField(max_length=20, default='')
    first_name = StringField(max_length=20, default='')
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "name": self.name,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "status": self.status
        }