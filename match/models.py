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
from django.conf import settings
from django.core.files import File
from django.contrib.postgres.fields import ArrayField, JSONField

from . import cvmatch
from .filename import image_upload_path
from register.models import Tank, Cucumber
from utilities.generators import generate_id

import logging
logger = logging.getLogger('django')


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

    def render(self, tex=False):
        """Return dict for rendering confirmation page."""
        matches = [{
            'id': m.identifier,
            'query_filename': os.path.basename(m.query_image.path),
            'query_img_uri': m.query_image.url,
            'query_img_path': m.query_image.path,
            'match_img_uri': m.best_match.source_image.url,
            'match_img_path': m.best_match.source_image.path,
            'identity': m.best_match.identifier,
            'match_details': m.best_match.details,
            'date_registered': m.best_match.date_created,
            "score": round(m.score),
            "score_color": score_color(m.score),
            'is_target': m.is_target
        } for m in self.get_matches()]

        failed = [{
            'query_filename': os.path.basename(f.query_image.path),
            "query_img_uri": f.query_image.url,
            "query_img_path": f.query_image.path,
            'exception': f.exception
        } for f in self.get_matches(failed=True)]

        data = {
            'tank_id': self.tank.identifier,
            'result_id': self.identifier,
            'matched': matches,
            'failed': failed,
        }

        if tex:
            result_url = (settings.BASE_URL
                          + "match/result/?id=%s" % self.identifier)
            data['tex_url'] = "\\href{%s}{%s}" % (result_url, result_url)

            for m in matches:
                m['query_img_tex'] = (
                    "\\includegraphics[width=30mm, height=20mm]{%s}" %
                    m['query_img_path']
                )
                m['match_img_tex'] = (
                    "\\includegraphics[width=30mm, height=20mm]{%s}" %
                    m['match_img_path']
                )

            for f in failed:
                f['query_img_tex'] = (
                    "\\includegraphics[width=30mm, height=20mm]{%s}" %
                    f['query_img_path']
                )
        return data


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
    rejected_matches = JSONField(default=list)  # [(score, cucumber_pk), ... ]
    backup_matches = JSONField(null=True)       # [(score, cucumber_pk), ... ]
    backup_index = models.IntegerField(default=0)
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
        logger.info("Image matching complete.")
        return match

    def fetch_next_match(self):
        """Fetch the next best match at the given index."""
        old_identity = self.best_match.identifier
        self.rejected_matches.insert(0, (self.score, self.best_match.id))
        self.score, subject_id = self.backup_matches.pop(self.backup_index)
        self.best_match = Cucumber.objects.get(pk=subject_id)
        logger.info("Fetching next match. Replacing %s with %s" % (
            old_identity,
            self.best_match.identifier
        ))
        return self.new_match_data()

    def fetch_previous_match(self):
        """Fetch the last best match at the given index."""
        old_identity = self.best_match.identifier
        self.backup_matches.insert(0, (self.score, self.best_match.id))
        self.score, subject_id = self.rejected_matches.pop(0)
        self.best_match = Cucumber.objects.get(pk=subject_id)
        logger.info("Fetching previous match. Replacing %s with %s" % (
            old_identity,
            self.best_match.identifier
        ))
        return self.new_match_data()

    def new_match_data(self):
        """Update match attributes and return new render data."""
        if self.best_match.identifier in self.record.targets:
            self.is_target = True
        else:
            self.is_target = False
        self.save()
        str_date = self.best_match.date_created.strftime('%d %b %Y')
        data = {
            "first": False,
            "last": False,
            "score": self.score,
            "score_color": score_color(self.score),
            "identity": self.best_match.identifier,
            "match_img_uri": self.best_match.source_image.url,
            'date_registered': str_date,
            'is_target': self.is_target,
        }
        if not len(self.rejected_matches):
            data['first'] = True
        if not len(self.backup_matches):
            data['last'] = True
        return data


def score_color(x):
    """Calculate color value for given score (red --> green)."""
    max_score = 1000
    if x > max_score:
        x = max_score
    g = round(200 * (x / 1000))
    r = round(100 - g / 2)
    b = 30
    return "rgba(%s,%s,%s,0.75)" % (r, g, b)
