from django.urls import path
from users.consumers.notify_consumer import NotifyConsumer

websocket_urlPattern = [
    path('ws/notify/', NotifyConsumer.as_asgi())
]