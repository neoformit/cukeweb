"""Store match jobs, run match and save results to DB.

An image-matching request is stored as a MatchSet, which is referenced by many
Match objects through a one-to-many relationship. A Match instance is
instantiated with a query image which is then run through the CV model to find
the best matching animal in the given tank. The results are then assigned to
the match instance and the model is saved.

The MatchSet object is also assigned the non-field attribute "report" which
references a MatchReport object. This holds the data needed for rendering the
result page and PDF report.
"""

import os
import cukecv
import traceback

from django.db import models
from django.core.files import File
from django.contrib.postgres.fields import ArrayField, JSONField

from . import cvmatch
from .filename import image_upload_path
from register.models import Tank, Cucumber
from utilities.generators import generate_id

import logging
logger = logging.getLogger('main')


def generate_matchset_id():
    """Return unique ID for new MatchSet instance."""
    return generate_id(MatchRecord)


def generate_result_id():
    """Return unique ID for new result instance."""
    return generate_id(Match)


class MatchRecord(models.Model):
    """Holds input params for an image match request.

    One-to-many with "Result" model which runs and stores the result for a
    single image match against the tank.
    """

    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    identifier = models.CharField(
        unique=True, max_length=100, default=generate_matchset_id)
    targets = ArrayField(models.CharField(max_length=75), null=True)

    @classmethod
    def create(cls, data, FILES):
        """Create a new Matchset and Result instance from clean form data."""
        record = cls.objects.create(
            tank=Tank.objects.get(identifier=data['tank_id']),
            targets=data['target_ids']
        )
        subjects = Cucumber.objects.filter(tank=record.tank)
        record.run(FILES, subjects)
        record.save()
        return record.identifier

    def run(self, FILES, subjects):
        """Create match instance and add to matches or failed."""
        for FILE in FILES.getlist('images'):
            Match.create(self, FILE, subjects)
        # matchset.resolve_conflicts()  <-- to do

    def resolve_conflicts(self):
        """Resolve multiple queries matching the same subject."""
        matches = Match.objects.filter(matchset=self)
        subjects = []
        conflicting = []
        for m in matches:
            if m.best_match.identity not in subjects:
                subjects.append(m.best_match.identity)
            else:
                conflicting.append(m.best_match.identity)
        # Resolve conflicts

    def get_matches(self, failed=False):
        """Return a list of successful match instances, targets first."""
        exc = not failed
        return (
            list(self.match_set.filter(
                exception__isnull=exc, is_target=True))
            + list(self.match_set.filter(
                exception__isnull=exc, is_target=False))
        )

    def render(self):
        """Return dict for rendering confirmation page."""
        matches = [{
            'query_filename': os.path.basename(m.query_image.path),
            'query_img_uri': m.query_image.url,
            'query_img_path': m.query_image.path,
            'date_registered': m.best_match.date_created,
            'id': m.best_match.identifier,
            "score": round(m.score),
            "score_color": score_color(m.score),
            'img_uri': m.best_match.source_image.url,
            'img_path': m.best_match.source_image.path,
            'is_target': m.is_target
        } for m in self.get_matches()]

        failed = [{
            'query_filename': os.path.basename(f.query_image.path),
            "query_img_uri": f.query_image.url,
            "query_img_path": f.query_image.path,
            'exception': f.exception
        } for f in self.get_matches(failed=True)]

        return {
            'tank_id': self.tank.identifier,
            'matched': matches,
            'failed': failed,
        }


class Match(models.Model):
    """A single image match result from a MatchSet instance."""

    # Required fields - pre-run
    record = models.ForeignKey(MatchRecord, on_delete=models.CASCADE)
    identifier = models.CharField(
        unique=True, max_length=100, default=generate_result_id)
    query_image = models.ImageField(upload_to=image_upload_path)
    # Fields populated post-run
    best_match = models.ForeignKey(
        Cucumber, on_delete=models.CASCADE, null=True)
    score = models.FloatField(null=True)
    is_target = models.BooleanField(default=False)
    backup_matches = JSONField(null=True)    # [(score, cucumber_pk), ... ]
    exception = models.TextField(null=True)
    traceback = models.TextField(null=True)

    @classmethod
    def create(cls, record, FILE, subjects):
        """Create and run match query with CV model."""
        try:
            match = cls.objects.create(
                # Identifier required for image_upload_path
                identifier=generate_result_id(),
                record=record,
                query_image=File(FILE)
            )

            logger.info("Extracting features from %s..." %
                        os.path.basename(match.query_image.path))
            query = cukecv.Cuke(match.query_image.path)

            logger.info("\tPerforming image match against database...")
            results = cvmatch.make(query, subjects)

            match.best_match = results[0][1]
            match.score = results[0][0]
            if match.best_match.identifier in record.targets:
                match.is_target = True
            match.backup_matches = [
                (score, subject.id)
                for score, subject in results[1:]
            ]
        except Exception as exc:
            match.exception = str(exc)
            match.traceback = traceback.format_exc()
            logger.error(match.traceback)
        match.save()
        return match

    def fetch_next_match(self, index):
        """Fetch the next best match at the given index."""
        score, subject_id = self.backup_matches[index]
        cuke = Cucumber.objects.get(pk=subject_id)
        return {
            "score": score,
            "identity": cuke.identifier,
            "img_uri": cuke.source_image.url
        }


def score_color(score):
    """Calculate color value for given score (red --> green)."""
    max_score = 1000
    if score > max_score:
        score = max_score
    green = int(200 * (score / max_score))
    red = 200 - green
    blue = 20
    return "rgba(%s,%s,%s,0.75)" % (red, green, blue)
