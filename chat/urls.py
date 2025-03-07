from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from chat import views


urlpatterns = [
    # Home
    path("", views.home, name="home"),
    path("remove_room/<int:id>/", views.remove_room, name="remove_room"),
    path("create_room", views.create_room, name="create_room"),
    # Rooms
    path("room/<int:id>/", views.room_view, name="room_view"),
    # Auth process
    path("register/", views.register_user, name="register-user"),
    path("login/", views.login_user, name="login-user"),
    path("logout/", LogoutView.as_view(), name="logout-user"),
    path("auth/", views.qr_code, name="auth"),
    path('metrics/', views.metrics_view, name='metrics'),
]
