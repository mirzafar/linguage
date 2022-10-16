from mongoengine import *


class Country(Document):
    title = StringField(required=True)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "title": self.title,
            "status": self.status
        }


class City(Document):
    title = StringField(required=True)
    country = ReferenceField('Country')
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "title": self.title,
            "country": self.country.serialize(),
            "status": self.status
        }


class Topic(Document):
    title = StringField(required=True, max_length=200)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "title": self.title,
            "status": self.status
        }


class Dictionary(Document):
    title = StringField(required=True, max_length=200)
    listening = StringField(max_length=200)
    topic = ReferenceField('Topic')
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "title": self.title,
            "listening": self.listening,
            "topic": self.topic.serialize(),
            "status": self.status
        }
