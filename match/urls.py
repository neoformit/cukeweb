"""URLconf for the match app."""

from . import views, async_requests
from django.urls import path

urlpatterns = [
    path("", views.query, name="match_query"),
    path("result/", views.result, name="match_result"),
    path("report/", views.report, name="match_report"),
    path("colors/", views.colors, name="colors"),
]

# Async request urls
urlpatterns += [
    path("fetchids/", async_requests.fetch_cuke_ids, name="fetch_ids"),
    path("reject/", async_requests.reject_match, name="reject_match"),
    path("sendmail/",
         async_requests.email_result_link, name="email_result_link"),
]
