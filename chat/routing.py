from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("wss/room/(?P<id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]
