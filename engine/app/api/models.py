from mongoengine import *
import datetime
from app.admin.models import User

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
    limit_count = IntField(default=0)
    active = IntField(default=0)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "title": self.title,
            "create_date": self.create_date.strftime("%b %d, %Y"),
            "status": self.status
        }


class LessonWord(Document):
    lesson = ReferenceField('Lesson', reverse_delete_rule=CASCADE)
    word = ReferenceField('Word', reverse_delete_rule=CASCADE)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "lesson": self.lesson.serialize(),
            "word": self.word.serialize(),
            "status": self.status
        }


class UserResult(Document):
    ball = IntField(default=0)
    data_start = DateTimeField()
    data_finish = DateTimeField()
    user = ReferenceField('User', reverse_delete_rule=CASCADE)
    lesson = ReferenceField('Lesson', reverse_delete_rule=CASCADE)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "ball": self.ball,
            "data_start": self.data_start,
            "data_finish": self.data_finish,
            "user": self.user.serialize(),
            "lesson": self.lesson.serialize(),
            "status": self.status
        }


class UserLesson(Document):
    userresult = ReferenceField('UserResult', reverse_delete_rule=CASCADE)
    lessonword = ReferenceField('LessonWord', reverse_delete_rule=CASCADE)
    level = IntField(default=0)
    user_otvet = StringField(max_length=200)
    flag = BooleanField(default=False)
    status = IntField(default=0)

    def serialize(self):
        return {
            "id": str(self.pk),
            "userresult": self.userresult.serialize(),
            "lessonword": self.lessonword.serialize(),
            "level": self.level,
            "user_otvet": self.user_otvet,
            "flag": self.flag,
            "status": self.status
        }


