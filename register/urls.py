"""URLconf for the register app."""

from . import views
from django.urls import path

urlpatterns = [
    path("", views.register, name="register"),
    path("confirm/", views.confirm, name="confirm"),
]
