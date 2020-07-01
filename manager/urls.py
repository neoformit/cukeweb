"""URLconf for the search app."""

from . import views, async_handlers
from django.urls import path

urlpatterns = [
    path("", views.manage, name="manage"),
]

# Async handlers
urlpatterns += [
    path("delete_tank/", async_handlers.delete_tank, name="delete_tank"),
    path("delete_cuke/", async_handlers.delete_cuke, name="delete_cuke"),
    path("update_cuke/", async_handlers.update_cuke, name="update_cuke"),
]
