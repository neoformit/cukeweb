"""Take requested tank and images and run match with CukeCV."""

import os
import cukecv
import string
import random
from operator import itemgetter

from django.conf import settings

import logging
logger = logging.getLogger('main')

alphanumeric = string.ascii_letters + string.digits


def make(query, subjects):
    """Run an image recognition search with given cuke instances."""
    results = []
    for subject in subjects:
        results.append((
            subject,
            query.match(cukecv.ReconstitutedCuke(subject)),
        ))
    results.sort(key=itemgetter(1), reverse=True)
    return results


class MatchReport:
    """Holds information about an image matching request."""

    def __init__(self, tank_id):
        """Initialize report with a tank name."""
        self.tank_id = tank_id
        self.matched = []
        self.failed = []

    def add(self, match):
        """Add a successful match instance to the report."""
        self.matched.append({
            'query_filename': match.query_image.name,
            'query_img_path': os.path.join(
                settings.MEDIA_ROOT,
                match.query_image.path
            ),
            'match_id': match.best_match.identifier,
            'match_img_path': os.path.join(
                settings.MEDIA_ROOT,
                match.best_match.source_image.path
            ),
            "score": match.score,
        })

    def fail(self, FILE, exc):
        """Add record of a failed query cuke render."""
        while True:
            temp_fname = ''.join([
                random.choice(alphanumeric) for i in range(12)
            ]) + '.jpg'  # 12 char random string file name
            temp_path = os.path.join(
                settings.MEDIA_ROOT, 'temp', 'images', temp_fname)
            if not os.path.exists(temp_path):
                break
        temp_uri = "%stemp/images/%s" % (settings.MEDIA_URL, temp_fname)
        save_temp(FILE, temp_path)
        self.failed.append({
            "filename": FILE.name,
            "img_uri": temp_uri,
            "img_path": temp_path,
            "message": str(exc)
        })

    def request_data(self):
        """Return dict for rendering confirmation page."""
        return {
            'tank_id': self.tank_id,
            'count': len(self.matched),
            'matched': self.matched,
            'failed': self.failed,
        }

    def report_data(self):
        """Render a pdf of this report."""
        return {
            'identifier': self.identifier,
            'tank_id': self.tank_id,
            'matches': self.matched,
            'failed': self.failed,
        }


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
