from sanic import Sanic
from .api.urls import api
from .rest.urls import rest
from .admin.urls import admin
from .loo.handlers import auth
from .loo.utils import util
from mongoengine import connect
from sanic import Blueprint
from pathlib import Path
import os
from settings import settings


def create_app():
    app = Sanic(__name__)
    app.config.AUTH_LOGIN_ENDPOINT = settings.get('auth', {}).get('redirect_url', '') or 'admin.login'


    ################## middleware

    ses = {}

    @app.middleware('request')
    async def add_sesion(request):
        request.ctx.session = ses

    ################## include urls
    app.blueprint(api)
    app.blueprint(rest)
    app.blueprint(admin)
    app.blueprint(util)

    ###################
    auth.setup(app)

    ################## static
    app.static('/static', './static')

    ################## connect db
    connect(db=settings.get('db', {}).get('name', '') or 'testdb',
            host=settings.get('db', {}).get('host', '') or '127.0.0.1',
            port=settings.get('db', {}).get('port', '') or 27017)

    return app
