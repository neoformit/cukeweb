"""Functions for managing temp files."""

import os
from django.conf import settings

import logging
logger = logging.getLogger('main')


def purge_temps(*dirs):
    """Delete all existing files in the given temp directories."""
    logger.info('Purging temp files from directories %s' %
                ', '.join(dirs))

    for d in dirs:
        path = os.path.join(settings.MEDIA_ROOT, 'temp', d)
        for f in os.listdir(path):
            fpath = os.path.join(path, f)
            try:
                os.remove(fpath)
            except PermissionError:
                logger.warning(
                    "Permission denied removing temp file %s" % fpath)
