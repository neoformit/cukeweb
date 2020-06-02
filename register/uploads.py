"""Functions relating to file uploads."""

import os
import string
import random

from django.conf import settings
from .models import Cucumber

import logging
logger = logging.getLogger('main')

alphanumeric = string.ascii_letters + string.digits


def register(FILES, tank):
    """Register the images to the given tank."""
    invalid = []
    success_count = 0
    for f in FILES.getlist('images'):
        print("Registering cucumber from image %s" % f.name)
        try:
            Cucumber.register(f, tank)
            success_count += 1
        except Exception as exc:
            # Usually NoCukeFoundError or DuplicateCucumberError
            temp_fname = ''.join([
                random.choice(alphanumeric) for i in range(12)
            ]) + '.jpg'
            temp_uri = "%stemp/%s" % (settings.MEDIA_URL, temp_fname)
            invalid.append({
                "name": f.name,
                "uri": temp_uri,
                "message": str(exc)
            })
            save_temp(f, temp_fname)
    return success_count, invalid


def save_temp(file, fname):
    """Save file as temp for display in confirmation page."""
    path = os.path.join(settings.MEDIA_ROOT, 'temp', fname)
    logger.info("Writing failed registration image %s\nPath: %s" %
                (fname, path))
    with open(path, 'wb') as temp:
        for chunk in file.chunks():
            temp.write(chunk)
