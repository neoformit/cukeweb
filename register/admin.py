"""Register models with the Django admin interface."""

from django.utils.html import format_html

from django.contrib import admin
from .models import Tank, Cucumber


class TankAdmin(admin.ModelAdmin):
    """Custom model admin for displaying Tanks in the admin interface."""

    list_display = ('identifier', 'date_created', 'cucumbers')

    def cucumbers(self, obj):
        """Show foreignkey cucumber_set count."""
        return format_html(
            '<p> Contains {count} cucumbers <p>',
            count=obj.cucumber_set.count()
        )


class CucumberAdmin(admin.ModelAdmin):
    """Custom model admin for displaying Cucumbers in the admin interface."""

    list_display = ('identifier', 'tank', 'date_created', 'image')

    def image(self, obj):
        """Display an image of the cucumber."""
        return format_html(
            '<img src="{img_uri}" style="width: 200px;"/>',
            img_uri=obj.url
        )


admin.site.register(Tank, TankAdmin)
admin.site.register(Cucumber, CucumberAdmin)
