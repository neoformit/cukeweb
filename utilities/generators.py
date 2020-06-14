"""Functions to generate variables."""

import string
import random

alphanumeric = string.ascii_letters + string.digits


def generate_id(model, field="identifier"):
    """Create a unique ID for a new model field."""
    while True:
        identifier = ''.join([
            random.choice(alphanumeric) for i in range(12)
        ])
        if not model.objects.filter(**{field: identifier}):
            return identifier
