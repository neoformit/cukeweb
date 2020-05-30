"""Functions relating to file uploads."""

import os
import string
import random
from cukecv.aux.exceptions import NoCukeFoundError
from django.conf import settings
from .models import Cucumber

alphanumeric = string.ascii_letters + string.digits


def register(FILES, tank):
    """Register the images to the given tank."""
    not_found = []
    for f in FILES.getlist('images'):
        print("Registering cucumber from image %s" % f.name)
        try:
            Cucumber.register(f, tank)
        except NoCukeFoundError:
            temp_name = ''.join([
                random.choice(alphanumeric) for i in range(12)
            ]) + '.jpg'
            temp_url = "%stemp/%s" % (settings.MEDIA_URL, temp_name)
            not_found.append((f.name, temp_name))
            save_temp(f, temp_url)
    return not_found


def save_temp(file, fname):
    """Save file as temp for display in confirmation page."""
    path = os.path.join(settings.MEDIA_ROOT, 'temp', fname)
    with open(path, 'rb+') as temp:
        for chunk in file.chunks():
            temp.write(chunk)
