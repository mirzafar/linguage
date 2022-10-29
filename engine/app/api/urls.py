from sanic import Blueprint
from sanic import response
from .views import *


api = Blueprint('api', url_prefix="/api")

api.add_route(HomeView.as_view(), "/", name="home")

api.add_route(CityView.as_view(), "/city", name="city")
api.add_route(CountryView.as_view(), "/country", name="country")

api.add_route(TopicView.as_view(), "/topic", name="topic")
api.add_route(WordView.as_view(), "/word", name="word")

api.add_route(LessonView.as_view(), "/lesson", name="lesson")
api.add_route(LessonWordView.as_view(), "/lesson-word/<lesson_id>", name="lesson-word")


