from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from chat import views


urlpatterns = [
    path("", views.home, name="home"),
    path('room/<int:id>/', views.room_view, name='room_view'),
    path('remove_room/<int:id>/', views.remove_room, name='remove_room'),
    path('create_room', views.create_room, name='create_room'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room_name>/', views.getMessages, name='getMessages'),
    #register
    path("register/", views.register_user, name="register-user"),
    #login
    path("login/", views.login_user, name="login-user"),
    path("logout/", LogoutView.as_view(), name="logout-user"),
    path("auth/", views.qr_code, name="auth"),
]