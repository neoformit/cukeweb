"""URLconf for the home app."""

from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),  # Defaults to login page
    path("info/", views.info, name="info"),
    path("login/", views.home, name="login"),
    path("logout/", views.logout, name="logout"),
]
