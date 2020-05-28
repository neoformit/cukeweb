"""Functions relating to file uploads."""

import os
from django.conf import settings


def image_upload_path(instance, filename):
    """When registering new Cucumbers, return the path for the image file."""
    extn = filename.split('.')[-1]
    return os.path.join(
        settings.MEDIA_ROOT,
        'registration',
        instance.tank.identifier,
        instance.identifier + extn,
    )
