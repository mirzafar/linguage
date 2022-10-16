from app import create_app
from settings import settings

app = create_app()

if __name__ == "__main__":

    app.run(host=settings.get('app', {}).get('host', '') or '0.0.0.0',
            port=settings.get('app', {}).get('port', '') or 8000,
            debug=settings.get('app', {}).get('debug', '') or True,
            auto_reload=settings.get('app', {}).get('auto_reload', '') or True)
