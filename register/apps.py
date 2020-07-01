from django.apps import AppConfig


class RegisterConfig(AppConfig):
    """Define app configuration at runtime."""

    name = 'register'

    def ready(self):
        """Load modules."""
        from . import signals
