from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import html
from jinja2 import Environment, PackageLoader, select_autoescape
from settings import ROOT_DIR
from sanic.response import HTTPResponse
from sanic_auth import Auth


auth = Auth()


ROOT_DIR = ROOT_DIR[:-7]
env = Environment(loader=PackageLoader('app', f'{ROOT_DIR}/templates'), autoescape=select_autoescape(["html", "xml"]))


class BaseHTTPView(HTTPMethodView):
    def render_template(self, template: str, request: Request, **kwargs) -> html:
        template = env.get_template(template)
        rendered = template.render(request=request, app=request.app, url_for=request.app.url_for, **kwargs)
        # return html(rendered)
        return HTTPResponse(rendered, content_type='text/html')


class BaseAPIView(BaseHTTPView):
    decorators = [auth.login_required()]


