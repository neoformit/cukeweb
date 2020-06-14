"""Define file paths for cucumber images."""

import os


def image_upload_path(instance, filename):
    """When registering new Cucumbers, return path for image file."""
    extn = '.' + filename.split('.')[-1]
    return os.path.join(
        'registration',
        instance.tank.identifier,
        instance.identifier + extn,
    )
