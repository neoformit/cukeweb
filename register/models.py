"""Django models provide an interface for the PostgreSQL database.

The Cucumber model integrates the cuke image recognition repository.
Images are rendered into Cuke objects which are then serialized for
storage in a django JSONField. The Cuke.from_dict method can then be used to
"reconstitute" a cuke from JSON storage. Importantly, source images are always
retained in a Django filefield for future reference (e.g. results interface)
and for debugging purposes.
"""

from cukecv.cukecv import Cuke

from django.db import models
from django.core.files import File
from django.db.utils import IntegrityError
from django.contrib.postgres.fields import JSONField

from .filename import image_upload_path
from cukeweb.exceptions import DuplicateCucumberError

import logging
logger = logging.getLogger(__name__)


class Tank(models.Model):
    """A culture tank to which Cucumbers are registered."""

    date_created = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=25, unique=True)


class Cucumber(models.Model):
    """A feature-extracted cucumber assigned to a tank."""

    identifier = models.CharField(max_length=75, unique=True)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    source_image = models.ImageField(upload_to=image_upload_path)
    features = JSONField(null=True)    # Serialized cukecv.Cuke instance

    @classmethod
    def register(cls, file, tank):
        """Register the cucumber on file to the given tank.

        Returns a list of errors resulting from Cuke rendering.
        """
        try:
            c = cls.objects.create(
                identifier=file.name.split('/')[-1].rsplit('.', 1)[0],
                tank=tank,
                source_image=File(file),    # from TemporaryUploadedFile
            )
            cuke = Cuke(c.source_image.name)
            c.features = cuke.to_dict()
            c.save()
        except IntegrityError:
            raise DuplicateCucumberError(
                "A cucumber with this identifier has already been registered."
                " Please try again with a different filename."
            )
        except Exception as exc:
            # Don't save cucumbers that were rejected by cukecv
            c.delete()
            raise exc
