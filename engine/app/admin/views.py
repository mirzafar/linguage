from app.loo.handlers import auth, BaseHTTPView, BaseAPIView
from sanic import response
from sanic.views import HTTPMethodView
from .models import *


class LoginView(BaseHTTPView):
    async def get(self, request):
        users = User.objects.filter().first()
        return self.render_template("auth/login.html", request=request, users=users)

    async def post(self, request):
        last_name = request.form.get('last_name', '')
        if last_name:
            user = User.objects.filter()
            if user:
                user = user[0]
                auth.login_user(request, user)
                return response.redirect('/api/')
        return response.json({"name": "world"})


class RegisterView(BaseHTTPView):
    async def get(self, request):
        return self.render_template("auth/register.html", request=request)

    async def post(self, request):
        last_name = request.form.get('last_name', '')
        name = "admin"

        cn = User()
        cn.last_name = last_name
        cn.name = name
        cn.save()

        print("***********")
        print(cn.id)

        return response.json({"name": "world"})


class LogoutView(BaseAPIView):
    async def get(self, request):
        auth.logout_user(request)
        return response.redirect('/admin/login')


class TestView(BaseAPIView):
    async def get(self, request):
        return response.json({"hello": "world"})