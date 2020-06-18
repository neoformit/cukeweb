"""Django models provide an interface for the PostgreSQL database.

The Cucumber model integrates the cuke image recognition repository.
Images are rendered into Cuke objects which are then serialized for
storage in a django JSONField. The Cuke.from_dict method can then be used to
"reconstitute" a cuke from JSON storage. Importantly, source images are always
retained in a Django filefield for future reference (e.g. results interface)
and for debugging purposes.
"""

import cukecv

from django.db import models
from django.core.files import File
from django.contrib.postgres.fields import JSONField

from .filename import image_upload_path
from cukeweb.exceptions import DuplicateCukeError

import logging
logger = logging.getLogger('django')


class Tank(models.Model):
    """A culture tank to which Cucumbers are registered."""

    date_created = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=25, unique=True)


class Cucumber(models.Model):
    """A feature-extracted cucumber assigned to a tank."""

    identifier = models.CharField(max_length=75)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    source_image = models.ImageField(upload_to=image_upload_path)
    features = JSONField(null=True)    # Serialized cukecv.Cuke instance

    @classmethod
    def register(cls, file, tank, infer_id=True, prefix_id=""):
        """Register the cucumber on file to the given tank.

        Returns a list of errors resulting from Cuke rendering.

        SHOULD MOVE TO INSTANCE METHOD OF TANK.
        """
        if infer_id:
            cid = file.name.split('/')[-1].rsplit('.', 1)[0]
        else:
            prefix = prefix_id or "cuke_"
            cid = cls.create_new_id(tank, prefix)
        if cls.objects.filter(tank=tank, identifier=cid):
            raise DuplicateCukeError(
                "A cucumber with this identifier has already been registered"
                " to this tank. Please try again with a different filename or"
                " choose to auto-generate identifiers during registration."
            )
        try:
            c = cls.objects.create(
                identifier=cid,
                tank=tank,
                source_image=File(file),    # from TemporaryUploadedFile
            )
            cuke = cukecv.Cuke(c.source_image.path)
            c.features = cuke.to_dict()
            c.save()
            logger.info('Registered cuke %s to tank %s' %
                        (c.identifier, tank.identifier))
            return c
        except Exception as exc:
            # Don't save cucumbers that were rejected by cukecv
            c.delete()
            logger.warning('Cuke registration failed: %s' % str(exc))
            raise exc

    @classmethod
    def create_new_id(cls, tank, prefix):
        """Return a unique id based on given prefix."""
        existing = cls.objects.filter(
            tank=tank, identifier__startswith=prefix).values_list(
            'identifier', flat=True)
        if existing:
            next_ix = max([int(x[-4:]) for x in existing]) + 1
            return prefix + ("0000" + str(next_ix))[-4:]
        return prefix + "0001"
