"""URLconf for the register app."""

from . import views, async_handlers
from django.urls import path

urlpatterns = [
    path("", views.register, name="register"),
    path("report/", views.report, name="register_report"),
]

# Asyc request endpoints
urlpatterns += [
    path("notify/", async_handlers.notify_admin, name="register_notify_admin"),
]
