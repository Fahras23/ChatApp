from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/room/(?P<id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]
