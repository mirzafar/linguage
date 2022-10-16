import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


settings = {
    'file_path': os.path.join(ROOT_DIR[:-7], 'static', 'uploads'),
    'db': {
        'name': 'testdb',
        'port': 27017,
        'host': '127.0.0.1'
    },
    'auth': {
        'redirect_url': 'admin.login'
    },
    'app': {
        'port': 8000,
        'host': '0.0.0.0',
        'debug': True,
        'auto_reload': True
    }
}
