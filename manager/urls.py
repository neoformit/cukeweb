"""URLconf for the search app."""

from . import views
from django.urls import path

urlpatterns = [
    path("", views.manage, name="manage"),
]
