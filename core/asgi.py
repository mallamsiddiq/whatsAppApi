# mysite/asgi.py
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from utils.middleware.SocketTokenAuth import TokenAuthMiddlewareStack

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

# import django
# django.setup()

django_asgi_app = get_asgi_application()

import chat.routing
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

