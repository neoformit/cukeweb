"""URLconf for the match app."""

from . import views, async_requests
from django.urls import path

urlpatterns = [
    path("", views.query, name="query"),
    path("result/", views.result, name="result"),
]

# Async request urls
urlpatterns += [
    path("fetchids/", async_requests.fetch_cuke_ids, name="fetch_ids"),
]
