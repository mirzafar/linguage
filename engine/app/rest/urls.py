from sanic import Blueprint
from .views import *

rest = Blueprint('rest',  url_prefix="/rest")

rest.add_route(open, "/", name="open")
rest.add_route(IndexView.as_view(), "/index", name="index")
