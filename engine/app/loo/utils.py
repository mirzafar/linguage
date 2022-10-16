import uuid
from settings import settings
from pathlib import Path
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json

util = Blueprint('util',  url_prefix="/")


class UploadView(HTTPMethodView):
    async def get(self, request):
        return json({"hello": "world"})

    async def post(self, request):
        logo = request.files and request.files['image']
        file_name = ''

        if logo:
            logo = logo[0]
            hashik = str(uuid.uuid4())
            ext = logo.name.split('.')[len(logo.name.split('.'))-1] #[::-1][0]
            file_name = f'{settings["file_path"]}/{hashik[:2]}/{hashik[2:4]}/{hashik}.{ext}'
            Path(f'{settings["file_path"]}/{hashik[:2]}/{hashik[2:4]}').mkdir(parents=True, exist_ok=True)
            with open(file_name, 'wb') as f:
                f.write(logo.body)

        return json({"file name": file_name.split('/')[-3:]})


util.add_route(UploadView.as_view(), "/upload", name="upload")