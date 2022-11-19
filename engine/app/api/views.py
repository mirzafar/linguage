from app.loo.handlers import BaseHTTPView, BaseAPIView
from sanic import response
from sanic.views import HTTPMethodView
from .models import *
from .utils import get_random_words, text_to_audio
from datetime import datetime


class HomeView(BaseHTTPView):
    async def get(self, request):
        return self.render_template("home.html", request=request)


###################################################################
class TopicView(BaseHTTPView):
    async def get(self, request):
        topics = Topic.objects.filter(status=0).order_by('-create_date')
        return self.render_template("topic.html", request=request, topics=topics)


###################################################################
class WordView(BaseHTTPView):
    async def get(self, request):
        topics = Topic.objects.filter(status=0)
        words = Word.objects.filter(status=0)
        return self.render_template("word.html", request=request, words=words, topics=topics)

    async def post(self, request):
        text = request.form.get('text', '')
        translate = request.form.get('translate', '')
        topic_id = request.form.get('topic', '')

        wr = Word()
        wr.text = text

        audio_name = text_to_audio(text, 'en')
        wr.audio = audio_name

        audio_transtale_name = text_to_audio(translate, 'ru')
        wr.audio_translate = audio_transtale_name

        wr.translate = translate
        wr.topic = Topic.objects.get(id=topic_id)
        wr.save()

        return response.json({"succes": True})


###################################################################
class LessonView(BaseHTTPView):
    async def get(self, request):
        lessons = Lesson.objects.filter(status=0)
        return self.render_template("lesson.html", request=request, lessons=lessons)


###################################################################
class TypeTranslateView(BaseHTTPView):
    async def get(self, request):
        items = Type.objects.filter(status=0).order_by('-create_date')
        return self.render_template("typetranslate.html", request=request, items=items)


###################################################################
class LessonWordView(BaseHTTPView):
    async def get(self, request, lesson_id):
        lesson = Lesson.objects.filter(id=lesson_id).first()
        lesson_words = LessonWord.objects.filter(status=0, lesson=lesson_id)
        lesson_words_id = []
        for i in lesson_words:
            lesson_words_id.append(i.word.id)
        words = Word.objects.filter(status=0, id__not__in=lesson_words_id)

        typelessons = TypeLesson.objects.filter(status=0, lesson=lesson_id)
        typelessons_ids = []
        for i in typelessons:
            typelessons_ids.append(i.type.id)

        types = Type.objects.filter(status=0, id__not__in=typelessons_ids)

        return self.render_template("lesson-word.html", request=request, words=words, lesson=lesson, lesson_words=lesson_words, types=types, typelessons=typelessons)


###################################################################
class TestView(BaseHTTPView):
    async def get(self, request, test_id):
        limit = int(request.args.get('limit', 1))
        current_page = int(request.args.get('page', 1))
        skip_count = (current_page - 1) * limit

        action = request.args.get('action', '')

        user = request.ctx.session.get('_auth')
        user_id = '6375166c3faaea6aed5ef007' #user.get('uid')

        tests = []

        compl_persent = 0

        if user_id:
            active_result = UserResult.objects.filter(status=0, user=user_id, lesson=test_id).order_by('level')
            current_lesson = Lesson.objects.get(id=test_id)
            current_lessonwords = LessonWord.objects.filter(status=0, lesson=current_lesson.id)
            count_userresult = UserResult.objects.filter(user=user_id, lesson=test_id).count()

            if active_result and current_lesson.active == 0:
                ari = active_result[0]
                compl_test_count = UserLesson.objects.filter(status=1, userresult=ari.id).count()
                all_test_count = UserLesson.objects.filter(userresult=ari.id).count()
                compl_persent = compl_test_count * 100 / all_test_count

                active_result_ids = []
                for i in active_result:
                    active_result_ids.append(i.id)
                tests = UserLesson.objects.filter(status=0, userresult__in=active_result_ids).order_by('userresult.level').skip(skip_count).limit(limit)
            else:
                if count_userresult < current_lesson.limit_count and current_lesson.active == 0:
                    if action == 'start' and current_lessonwords:
                        active_result_type = TypeLesson.objects.filter(status=0, lesson=current_lesson.id)
                        if active_result_type:
                            types = []
                            tests = []
                            for art in active_result_type:
                                types.append(art.id)

                            ur = UserResult()
                            ur.user = User.objects.get(status=0, id=user_id)
                            ur.lesson = Lesson.objects.get(status=0, id=test_id)
                            ur.data_start = datetime.now()
                            ur.lesson_types = types
                            ur.save()

                            for tp in types:
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
                                    ul.typelesson = TypeLesson.objects.get(status=0, id=tp)
                                    ul.save()
                            test = UserLesson.objects.filter(status=0, userresult=ur.id).order_by('level')
                            for i in test:
                                tests.append(i)
                        return response.redirect(f'/api/test/{test_id}')
        return self.render_template("tests.html", request=request, tests=tests, lesson_id=test_id, compl_persent=compl_persent)

    async def post(self, request, test_id):
        action = request.form.get('action', '')
        userflag = False
        success = False
        errors = []
        if action == 'check':
            userlesson_id = request.form.get('userlesson_id', '')
            user_otvet = request.form.get('user_otvet', '')
            lesson_id = request.form.get('lesson_id', '')
            typelesson_id = request.form.get('typelesson_id', '')

            if user_otvet and typelesson_id:
                success = True
                userlesson = UserLesson.objects.get(status=0, id=userlesson_id)
                if userlesson:
                    userlesson.user_otvet = user_otvet
                    typelesson = TypeLesson.objects.get(id=typelesson_id)
                    if typelesson and typelesson.type.title == 'text-translate':
                        if userlesson.lessonword.word.translate == user_otvet:
                            userflag = True
                            userlesson.flag = True
                            userlesson.userresult.ball += 1
                            userlesson.userresult.save()
                        else:
                            userflag = False
                            userlesson.flag = False
                    elif typelesson and typelesson.type.title == 'translate-text':
                        if userlesson.lessonword.word.text == user_otvet:
                            userflag = True
                            userlesson.flag = True
                            userlesson.userresult.ball += 1
                            userlesson.userresult.save()
                        else:
                            userflag = False
                            userlesson.flag = False
                    elif typelesson and typelesson.type.title == 'audio-text':
                        if userlesson.lessonword.word.text == user_otvet:
                            userflag = True
                            userlesson.flag = True
                            userlesson.userresult.ball += 1
                            userlesson.userresult.save()
                        else:
                            userflag = False
                            userlesson.flag = False
                    elif typelesson and typelesson.type.title == 'audio-translate':
                        if userlesson.lessonword.word.translate == user_otvet:
                            userflag = True
                            userlesson.flag = True
                            userlesson.userresult.ball += 1
                            userlesson.userresult.save()
                        else:
                            userflag = False
                            userlesson.flag = False
                    elif typelesson and typelesson.type.title == 'audio-translate-text':
                        if userlesson.lessonword.word.text == user_otvet:
                            userflag = True
                            userlesson.flag = True
                            userlesson.userresult.ball += 1
                            userlesson.userresult.save()
                        else:
                            userflag = False
                            userlesson.flag = False
                    userlesson.status = 1
                    userlesson.save()

                    user_id = '6375166c3faaea6aed5ef007'
                    userresult = UserResult.objects.get(status=0, user=user_id, lesson=lesson_id)
                    userlessons = UserLesson.objects.filter(status=0, userresult=userresult)
                    if not userlessons:
                        userresult.data_finish = datetime.now()
                        userresult.status = 1
                        userresult.save()
            else:
                errors.append("напешите ответ")

        return response.json({"success": success, "flag": userflag, "errors": errors})


###################################################################
class ResultView(BaseHTTPView):
    async def get(self, request):
        user = request.ctx.session.get('_auth')
        user_id = '6375166c3faaea6aed5ef007'  # user.get('uid')
        user_name = 'student'  # user.get('name')

        items = []
        if user_name == 'student':
            userresult = UserResult.objects.filter(user=user_id)
        else:
            userresult = UserResult.objects.filter()

        for i in userresult:
            type_userresult = TypeLesson.objects.filter(id__in=i.lesson_types)
            count_type = {}
            for k in type_userresult:
                count_type[k.type.title] = {
                    'flag_true': UserLesson.objects.filter(userresult=i.id, flag=True, typelesson=k.id).count(),
                    'flag_false': UserLesson.objects.filter(userresult=i.id, flag=False, typelesson=k.id).count(),
                }
            obj = {
                "id": i.id,
                "ball": i.ball,
                "data_start": i.data_start,
                "data_finish": i.data_finish,
                "user": i.user,
                "lesson": i.lesson,
                "count_type": count_type,
                "count_true": UserLesson.objects.filter(userresult=i.id, flag=True).count(),
                "count_false": UserLesson.objects.filter(userresult=i.id, flag=False).count(),
                "status": i.status,
            }
            items.append(obj)

        return self.render_template("result.html", request=request, items=items)
