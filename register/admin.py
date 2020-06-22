"""Register models with the Django admin interface."""

from django.utils.html import format_html

from django.contrib import admin
from .models import Tank, Cucumber


class TankAdmin(admin.ModelAdmin):
    """Custom model admin for displaying Tanks in the admin interface."""

    list_display = ('identifier', 'date_created', 'occupants')

    def occupants(self, obj):
        """Show foreignkey cucumber_set count."""
        return format_html(
            '<p> {count} animals <p>',
            count=obj.cucumber_set.count()
        )


class CucumberAdmin(admin.ModelAdmin):
    """Custom model admin for displaying Cucumbers in the admin interface."""

    list_display = ('identifier', 'tank_id', 'date_created', 'image')

    def tank_id(self, obj):
        """Display tank ID."""
        return format_html(
            '<p> Tank "{tank_id}" </p>',
            tank_id=obj.tank.identifier
        )

    def image(self, obj):
        """Display an image of the cucumber."""
        return format_html(
            '<img src="{img_uri}" style="width: 150px;"/>',
            img_uri=obj.source_image.url
        )
    tank_id.short_description = "Tank"
    image.short_description = "Source image"

admin.site.register(Tank, TankAdmin)
admin.site.register(Cucumber, CucumberAdmin)
