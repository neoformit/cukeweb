"""Register models with the Django admin interface."""

from django.contrib import admin
from .models import Match, MatchRecord

admin.site.register(Match)
admin.site.register(MatchRecord)
