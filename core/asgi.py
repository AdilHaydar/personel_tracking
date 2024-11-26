import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .routing import websocket_urlPattern
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
#from chat.middleware.token_auth_middleware import AuthMiddlewareStack
# from games.middleware.token_auth_middleware import TokenAuthMiddleware




application = ProtocolTypeRouter({
    "http":django_asgi_app,
    # "websocket":AllowedHostsOriginValidator(URLRouter(websocket_urlPattern)),
    #"websocket":AuthMiddlewareStack(URLRouter(websocket_urlPattern)),
    "websocket":AuthMiddlewareStack(URLRouter(websocket_urlPattern)),
})


#AllowedHostsOriginValidator ile postmanden gelen isteği blokluyoruz. postman attığım istek 403 forbidden hatası versin istemiyorsam settings.py da ALLOWED_HOSTS = ['*'] yapmalıyım.