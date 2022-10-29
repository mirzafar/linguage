from app.loo.handlers import BaseHTTPView, BaseAPIView
from sanic import response
from sanic.views import HTTPMethodView
from .models import *


class HomeView(BaseHTTPView):
    async def get(self, request):
        return self.render_template("home.html", request=request)


class CountryView(BaseHTTPView):

    async def get(self, request):
        countrys = Country.objects.filter()
        return self.render_template("country.html", request=request, countrys=countrys)

    async def post(self, request):
        title = request.form.get('title', '')

        cn = Country()
        cn.title = title
        cn.save()

        return response.json({"name": title})


class CityView(BaseAPIView):
    async def get(self, request):
        countrys = Country.objects.filter()
        citys = City.objects.filter()
        return self.render_template("city.html", request=request, citys=list(citys), countrys=countrys)

    async def post(self, request):
        title = request.form.get('title', '')
        country_id = request.form.get('country', '')

        cn = City(title=title, country=country_id)
        cn.save()

        return response.json({"name": title})


###################################################################
class TopicView(BaseHTTPView):
    async def get(self, request):
        topics = Topic.objects.filter(status=0).order_by('+date')
        return self.render_template("topic.html", request=request, topics=topics)


###################################################################
class WordView(BaseHTTPView):
    async def get(self, request):
        topics = Topic.objects.filter(status=0)
        words = Word.objects.filter(status=0)
        return self.render_template("word.html", request=request, words=words, topics=topics)


###################################################################
class LessonView(BaseHTTPView):
    async def get(self, request):
        lessons = Lesson.objects.filter(status=0)
        return self.render_template("lesson.html", request=request, lessons=lessons)


###################################################################
class LessonWordView(BaseHTTPView):
    async def get(self, request, lesson_id):
        lesson = Lesson.objects.filter(id=lesson_id).first()
        lesson_words = LessonWord.objects.filter(status=0, lesson=lesson_id)
        lesson_words_id = []
        for i in lesson_words:
            lesson_words_id.append(i.word.id)
        print(lesson_words_id)
        words = Word.objects.filter(status=0, id__not__in=lesson_words_id)

        return self.render_template("lesson-word.html", request=request, words=words, lesson=lesson, lesson_words=lesson_words)
