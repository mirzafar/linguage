from sanic import Blueprint
from sanic import response
from .views import *


api = Blueprint('api', url_prefix="/api")

api.add_route(HomeView.as_view(), "/", name="home")
api.add_route(CountryView.as_view(), "/country", name="country")
api.add_route(CityView.as_view(), "/city", name="country")

