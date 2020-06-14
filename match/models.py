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
import string
import cukecv
import traceback
from cukecv.aux.exceptions import NoCukeFoundError

from django.db import models
from django.conf import settings
from django.core.files import File
from django.contrib.postgres.fields import ArrayField, JSONField

from . import cvmatch
from .filename import image_upload_path
from register.models import Tank, Cucumber
from utilities.generators import generate_id

import logging
logger = logging.getLogger('main')

alphanumeric = string.ascii_letters + string.digits


def generate_matchset_id():
    """Return unique ID for new MatchSet instance."""
    return generate_id(MatchSet)


def generate_result_id():
    """Return unique ID for new result instance."""
    return generate_id(Match)


class MatchSet(models.Model):
    """Holds input params for an image match request.

    One-to-many with "Result" model which runs and stores the result for a
    single image match against the tank.
    """

    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    identifier = models.CharField(unique=True, default=generate_matchset_id)
    targets = ArrayField(models.CharField(max_length=75), null=True)

    @classmethod
    def create(cls, data, FILES):
        """Create a new Matchset and Result instance from clean form data."""
        matchset = cls.objects.create(
            tank=Tank.objects.get(identifier=data['tank_id']),
            targets=data['target_ids']
        )
        matchset.report = cvmatch.MatchReport(data['tank_id'])
        subjects = Cucumber.objects.filter(tank=matchset.tank)

        for FILE in FILES.getlist('images'):
            try:
                match = Match.create(matchset, FILE, subjects)
                matchset.report.add(match)
            except NoCukeFoundError as exc:
                matchset.report.fail(FILE, exc)
            except Exception as exc:
                matchset.report.fail(FILE, exc)
                logger.error(traceback.format_exc())
        # matchset.resolve_conflicts()  <-- to do
        return matchset

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
        # while true: resolve conflicts


class Match(models.Model):
    """A single image match result from a MatchSet instance."""

    # Required fields - pre-run
    identifier = models.CharField(unique=True, default=generate_result_id)
    matchset = models.ForeignKey(MatchSet, on_delete=models.CASCADE)
    query_image = models.ImageField(upload_to=image_upload_path)
    # Populated post-run
    best_match = models.ForeignKey(
        Cucumber, on_delete=models.CASCADE, null=True)
    score = models.FloatField()
    is_target = models.BooleanField(default=False)
    backup_matches = JSONField(null=True)    # Match scores, cucumber ids

    @classmethod
    def create(cls, matchset, FILE, subjects):
        """Create and run match query with CV model."""
        match = cls.objects.create(
            matchset=matchset,
            query_image=File(FILE),
        )
        query = cukecv.Cuke(match.query_image.file)
        results = cvmatch.make(query, subjects)
        match.best_match = results[0][0]
        if match.best_match.identity in matchset.targets:
            match.is_target = True
        match.score = results[0][1]
        match.backup_matches = [
            (score, subject.id)
            for score, subject in results[1:]
        ]
        return match

    def fetch_next_match(self, index):
        """Fetch the next best match at the given index."""
        score, subject_id = self.backup_matches[index]
        cuke = Cucumber.objects.get(pk=subject_id)
        return {
            "score": score,
            "identity": cuke.identifier,
            "img_uri": os.path.join(
                settings.MEDIA_URL,
                cuke.source_image.img_path
            )
        }
