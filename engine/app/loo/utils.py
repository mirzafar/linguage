import uuid
from settings import settings
from pathlib import Path
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json
import sys
from app.api.models import *
import string

util = Blueprint('util',  url_prefix="/")


#############################################################################################################
class UploadView(HTTPMethodView):
    async def get(self, request):
        return json({"hello": "world"})

    async def post(self, request):
        file = request.files and request.files['file']
        file_name = ''

        if file:
            logo = file[0]
            hashik = str(uuid.uuid4())
            ext = logo.name.split('.')[len(logo.name.split('.'))-1] #[::-1][0]
            file_name = f'{settings["file_path"]}/{hashik[:2]}/{hashik[2:4]}/{hashik}.{ext}'
            Path(f'{settings["file_path"]}/{hashik[:2]}/{hashik[2:4]}').mkdir(parents=True, exist_ok=True)
            with open(file_name, 'wb') as f:
                f.write(logo.body)
            return_name = f'{hashik[:2]}/{hashik[2:4]}/{hashik}.{ext}'
            print(return_name)

        return json({"file name": return_name})


util.add_route(UploadView.as_view(), "/upload", name="upload")


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


#############################################################################################################
class CollectionAddView(HTTPMethodView):
    async def post(self, request, collection_name, action):
        if action == 'add':
            flag = True

            form_datas = request.form
            undefine = form_datas.get('undefined')
            if undefine:
                del form_datas['undefined']

            cn = str_to_class(collection_name)()

            for fd in form_datas:
                try:
                    ty = str_to_class(string.capwords(fd, sep=None)).objects.filter(id=form_datas.get(fd)).first()
                    cn[fd] = ty
                except:
                    cn[fd] = form_datas.get(fd)
            cn.save()

            return json({"succes": flag})
        else:
            flag = True

            form_datas = request.form
            undefine = form_datas.get('undefined')
            if undefine:
                del form_datas['undefined']
            print(form_datas)
            status = request.form.get("status")
            if status:
                cn = str_to_class(collection_name)(id=action)
                cn.delete()
            else:
                cn = str_to_class(collection_name)(id=action)
                for fd in form_datas:
                    try:
                        ty = str_to_class(string.capwords(fd, sep=None)).objects.filter(id=form_datas.get(fd)).first()
                        cn[fd] = ty
                    except:
                        cn[fd] = form_datas.get(fd)
                cn.save()

            return json({"succes": flag})


util.add_route(CollectionAddView.as_view(), "/collection/<collection_name>/<action>/", name="upload")

