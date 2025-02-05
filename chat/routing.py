from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/room/<str:id>/', consumers.ChatConsumer.as_asgi()),
]