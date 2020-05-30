"""Django models provide an interface for the PostgreSQL database.

The Cucumber model integrates the cuke image recognition repository.
Images are rendered into Cuke objects which are then serialized for
storage in a django JSONField. The Cuke.from_dict method can then be used to
"reconstitute" a cuke from JSON storage. Importantly, source images are always
retained in a Django filefield for future reference (e.g. results interface)
and for debugging purposes.
"""

import traceback
from cukecv.cucumber import Cuke

from django.db import models
from django.core.files import File
from django.contrib.postgres.fields import JSONField

from .filename import image_upload_path

import logging
logger = logging.getLogger(__name__)


class Tank(models.Model):
    """A culture tank to which Cucumbers are registered."""

    date_created = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=25)


class Cucumber(models.Model):
    """A feature-extracted cucumber assigned to a tank."""

    identifier = models.CharField(max_length=75)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    source_image = models.ImageField(upload_to=image_upload_path)
    features = JSONField(null=True)    # Serialized cukecv.Cuke instance

    @classmethod
    def register(cls, file, tank):
        """Register the cucumber on file to the given tank.

        Returns a list of errors resulting from Cuke rendering.
        """
        c = cls.objects.create(
            identifier=file.name.split('/')[-1].rsplit('.', 1)[0],
            tank=tank,
            source_image=File(file),    # from TemporaryUploadedFile
        )
        cuke = Cuke(c.source_image.name)
        c.features = cuke.to_dict()
        c.save()
