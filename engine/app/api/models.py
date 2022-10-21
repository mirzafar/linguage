from mongoengine import *
import datetime


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


#######################################################
class Topic(Document):
    title = StringField(required=True, max_length=200)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "title": self.title,
            "status": self.status
        }


class Word(Document):
    text = StringField(required=True, max_length=200)
    audio = StringField(max_length=2000)
    translate = StringField(max_length=200)
    audio_translate = StringField(max_length=200)
    topic = ReferenceField(Topic, reverse_delete_rule=CASCADE)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "text": self.text,
            "audio": self.audio,
            "translate": self.translate,
            "audio_translate": self.audio_translate,
            "topic": self.topic.serialize(),
            "status": self.status
        }


class Lesson(Document):
    title = StringField(required=True, max_length=200)
    create_date = DateTimeField(default=datetime.datetime.utcnow)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "title": self.title,
            "create_date": self.create_date.strftime("%b %d, %Y"),
            "status": self.status
        }


class LessonWord(Document):
    lesson_id = ReferenceField('Lesson')
    word_id = ReferenceField('Word')
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "lesson_id": self.lesson_id.serialize(),
            "word_id": self.word_id.serialize(),
            "status": self.status
        }

