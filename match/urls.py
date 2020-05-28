"""URLconf for the match app."""

from . import views
from django.urls import path

urlpatterns = [
    path("", views.input, name="input"),
    path("result", views.result, name="result"),
]
