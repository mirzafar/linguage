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
