"""Functions to generate variables."""

import string
import random


def generate_id(model, field="identifier"):
    """Create a unique ID for a new model instance."""
    alphanumeric = string.ascii_letters + string.digits
    while True:
        identifier = ''.join([
            random.choice(alphanumeric) for i in range(12)
        ])
        if not model.objects.filter(**{field: identifier}).count():
            return identifier
