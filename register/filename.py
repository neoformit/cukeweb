"""Define file paths for cucumber images."""

import os
from django.conf import settings


def image_upload_path(instance, filename):
    """When registering new Cucumbers, return path for image file."""
    extn = '.' + filename.split('.')[-1]
    return os.path.join(
        settings.MEDIA_ROOT,
        'registration',
        instance.tank.identifier,
        instance.identifier + extn,
    )
