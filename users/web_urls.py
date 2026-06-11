from django.urls import path
from .views import web_login_view, web_logout_view, web_register_view

urlpatterns = [
    path("login/", web_login_view, name="login"),
    path("logout/", web_logout_view, name="logout"),
    path("register/", web_register_view, name="register"),
]