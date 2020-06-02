"""Register models with the Django admin interface."""

from django.contrib import admin

from .models import Tank, Cucumber


admin.site.register(Tank)
admin.site.register(Cucumber)
