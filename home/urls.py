"""URLconf for the home app."""

from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("info/", views.info, name="info"),
]
