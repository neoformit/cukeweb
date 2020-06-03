"""URLconf for the register app."""

from . import views
from django.urls import path

urlpatterns = [
    path("", views.register, name="register"),
    path("report/", views.report, name="register_report"),
]
