from app.loo.handlers import BaseHTTPView
from sanic import response
from .models import *


def open(request):
    return response.json({"message": "rest"})


class IndexView(BaseHTTPView):
    async def get(self, request):
        return self.render_template("home.html", request=request, ups="pop")

