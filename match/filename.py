"""Define file paths for cucumber images."""

import os


def image_upload_path(instance, filename):
    """When creating new match results, return path for query image file."""
    return os.path.join(
        'match',
        instance.record.identifier,
        filename
    )
