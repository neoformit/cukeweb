"""Define file paths for cucumber images."""

import os
from django.conf import settings


def image_upload_path(instance, filename):
    """When creating new match results, return path for query image file."""
    extn = '.' + filename.split('.')[-1]
    return os.path.join(
        settings.MEDIA_ROOT,
        'match',
        instance.matchset.identifier,
        instance.identifier + extn,
    )
