"""Custom templates filters."""

from django import template

register = template.Library()


@register.filter
def texsafe(value):
    """Escape underscores during tex rendering."""
    return value.replace("_", "\\_")
