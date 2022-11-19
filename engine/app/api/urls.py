from sanic import Blueprint
from sanic import response
from .views import *


api = Blueprint('api', url_prefix="/api")

api.add_route(HomeView.as_view(), "/", name="home")

api.add_route(TopicView.as_view(), "/topic", name="topic")
api.add_route(WordView.as_view(), "/word", name="word")

api.add_route(ResultView.as_view(), "/result", name="result")

api.add_route(LessonView.as_view(), "/lesson", name="lesson")
api.add_route(LessonWordView.as_view(), "/lesson-word/<lesson_id>", name="lesson-word")

api.add_route(TypeTranslateView.as_view(), "/typetranslate/", name="typetranslate")

api.add_route(TestView.as_view(), "/test/<test_id>", name="test")


