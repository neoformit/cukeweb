"""Functions relating to file uploads."""

import os
import string
import random
import traceback

from cukecv.aux.exceptions import NoCukeFoundError

from django.conf import settings
from cukeweb.exceptions import DuplicateCukeError
from .models import Cucumber

import logging
logger = logging.getLogger('main')

alphanumeric = string.ascii_letters + string.digits


class Registration:
    """Holds information about cucumber registration event."""

    def __init__(self, tank_id):
        """Initialize report with a tank name."""
        self.identifier = ''.join([
            random.choice(alphanumeric) for i in range(12)
        ])
        self.tank_id = tank_id
        self.registered = []
        self.failed = []

    def add(self, cucumber):
        """Add a successfully registered cucumber instance."""
        self.registered.append({
            'id': cucumber.identifier,
            'filename': cucumber.source_image.name,
            'img_path': os.path.join(
                settings.MEDIA_ROOT,
                cucumber.source_image.path
            ),
        })

    def fail(self, file, exc):
        """Add record of a failed registration."""
        temp_fname = ''.join([
            random.choice(alphanumeric) for i in range(12)
        ]) + '.jpg'  # 12 char random string file name
        temp_uri = "%stemp/images/%s" % (settings.MEDIA_URL, temp_fname)
        temp_path = os.path.join(settings.MEDIA_ROOT,
                                 'temp', 'images', temp_fname)
        save_temp(file, temp_path)
        self.failed.append({
            "filename": file.name,
            "img_uri": temp_uri,
            "img_path": temp_path,
            "message": str(exc)
        })

    def request_data(self):
        """Return dict for rendering confirmation page."""
        return {
            'tank_id': self.tank_id,
            'count': len(self.registered),
            'failed': self.failed,
        }

    def report_data(self):
        """Render a pdf of this report."""
        return {
            'identifier': self.identifier,
            'tank_id': self.tank_id,
            'registrations': self.registered,
            'failed': self.failed,
        }


def register(FILES, tank, infer_id=True, prefix_id=""):
    """Register the images to the given tank."""
    purge_temps(['images', 'reports'])
    report = Registration(tank.identifier)

    for f in FILES.getlist('images'):
        print("Registering cucumber from image %s" % f.name)
        try:
            c = Cucumber.register(f, tank, infer_id=infer_id,
                                  prefix_id=prefix_id)
            report.add(c)
        except (NoCukeFoundError, DuplicateCukeError) as exc:
            report.fail(f, exc)
        except Exception as exc:
            logger.error(traceback.format_exc())
            report.fail(f, exc)
    return report


def save_temp(file, path):
    """Save file as temp for display in confirmation page."""
    logger.info("Writing failed registration image: %s" % path)
    with open(path, 'wb') as temp:
        for chunk in file.chunks():
            temp.write(chunk)


def purge_temps(dirs):
    """Delete all existing files in the given temp directories."""
    if type(dirs) is not list:
        dirs = [dirs]
    logger.info('Purging temp files from directory %s' %
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
                pass
