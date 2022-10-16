from sanic import Blueprint
from .views import *


admin = Blueprint('admin',  url_prefix="/admin")


admin.add_route(LoginView.as_view(), "/login", name="login")
admin.add_route(RegisterView.as_view(), "/register", name="register")
admin.add_route(LogoutView.as_view(), "/logout", name="logout")
admin.add_route(TestView.as_view(), "/test", name="test")