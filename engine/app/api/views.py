from app.loo.handlers import BaseHTTPView, BaseAPIView
from sanic import response
from sanic.views import HTTPMethodView
from .models import *
from .utils import get_random_words
from datetime import datetime


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
class ResultView(BaseHTTPView):
    async def get(self, request):
        items = []
        userresult = UserResult.objects.filter()
        userlesson = UserLesson.objects.filter()
        for i in userresult:
            obj = {
                "id": i.id,
                "ball": i.ball,
                "data_start": i.data_start,
                "data_finish": i.data_finish,
                "user": i.user,
                "lesson": i.lesson,
                "count_true": UserLesson.objects.filter(userresult=i.id, flag=True).count(),
                "count_false": UserLesson.objects.filter(userresult=i.id, flag=False).count(),
                "status": i.status,
            }
            items.append(obj)

        return self.render_template("result.html", request=request, items=items, userlesson=userlesson)


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


###################################################################
class TestView(BaseHTTPView):
    async def get(self, request, test_id):
        limit = int(request.args.get('limit', 2))
        current_page = int(request.args.get('page', 1))
        skip_count = (current_page - 1) * limit

        action = request.args.get('action', '')

        user = request.ctx.session.get('_auth')
        user_id = '636d5eab89960eb966f00619' #user.get('uid')

        tests = []

        if user_id:
            active_result = UserResult.objects.filter(status=0, user=user_id, lesson=test_id)
            count_userresult = UserResult.objects.filter(status__gte=0, user=user_id, lesson=test_id).count()
            print("========>")
            print(count_userresult)
            current_lesson = Lesson.objects.get(id=test_id)
            print(current_lesson.limit_count)

            if active_result and current_lesson.active == 0:
                active_result = active_result[0]
                tests = UserLesson.objects.filter(status=0, userresult=active_result.id)
            else:
                if count_userresult < current_lesson.limit_count and current_lesson.active == 0:
                    if action == 'start':
                        ur = UserResult()
                        ur.user = User.objects.get(status=0, id=user_id)
                        ur.lesson = Lesson.objects.get(status=0, id=test_id)
                        ur.data_start = datetime.now()
                        ur.save()

                        lessonwords = LessonWord.objects.filter(status=0, lesson=test_id)
                        lessonword_ids = []
                        for i in lessonwords:
                            lessonword_ids.append(i.id)
                        test_ids = get_random_words(lessonword_ids)
                        level = 1
                        for i in test_ids:
                            ul = UserLesson()
                            ul.userresult = UserResult.objects.get(status=0, id=ur.id)
                            ul.lessonword = LessonWord.objects.get(status=0, id=i)
                            ul.level = level
                            level += 1
                            ul.save()
                        tests = UserLesson.objects.filter(status=0, userresult=ur.id)

        return self.render_template("tests.html", request=request, tests=tests, lesson_id=test_id)

    async def post(self, request, test_id):
        action = request.form.get('action', '')
        userflag = False
        if action == 'check':
            userlesson_id = request.form.get('userlesson_id', '')
            user_otvet = request.form.get('user_otvet', '')
            lesson_id = request.form.get('lesson_id', '')

            print("---->")
            print(user_otvet)
            print(userlesson_id)

            errors = []

            if user_otvet:
                userlesson = UserLesson.objects.get(status=0, id=userlesson_id)
                if userlesson:
                    userlesson.user_otvet = user_otvet
                    if userlesson.lessonword.word.translate == user_otvet:
                        userflag = True
                        userlesson.flag = True
                        userlesson.userresult.ball += 1
                        userlesson.userresult.save()
                    else:
                        userflag = False
                        userlesson.flag = False
                    userlesson.status = 1
                    userlesson.save()

                    user_id = '636d5eab89960eb966f00619'
                    userresult = UserResult.objects.get(status=0, user=user_id, lesson=lesson_id)
                    userlessons = UserLesson.objects.filter(status=0, userresult=userresult)
                    if not userlessons:
                        userresult.data_finish = datetime.now()
                        userresult.status = 1
                        userresult.save()
            else:
                errors.append("напешите ответ")

        return response.json({"success": True, "flag": userflag})

