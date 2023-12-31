from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from chat import views


urlpatterns = [
    path("", views.home, name="home"),
    path('room/<str:room_name>/', views.room_view, name='room_view'),
    path('create_room', views.create_room, name='create_room'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room_name>/', views.getMessages, name='getMessages'),
    #login
    path("login/", LoginView.as_view
         (template_name="chat/login.html"), name="login-user"),
    path("logout/", LogoutView.as_view(), name="logout-user"),
]