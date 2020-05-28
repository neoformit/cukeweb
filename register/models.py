"""Django models provide an interface for the PostgreSQL database.

The Cucumber model integrates the cuke image recognition repository.
Images are rendered into Cuke objects which are then serialized for
storage in a django JSONField. The Cuke.from_dict method can then be used to
"reconstitute" a cuke from JSON storage. Importantly, source images are always
retained in a Django filefield for future reference (e.g. results interface)
and for debugging purposes.
"""

from cuke import Cuke

from django.db import models
from django.contrib.postgres.fields import JSONField

from .uploads import image_upload_path


class Tank(models.Model):
    """A culture tank to which Cucumbers are registered."""

    date_created = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=25)


class Cucumber(models.Model):
    """A feature-extracted cucumber assigned to a tank."""

    identifier = models.CharField(max_length=75)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    source_image = models.FileField(upload_to=image_upload_path)
    features = JSONField()    # Serialized Cuke instance

    @classmethod
    def register(cls, file, tank):
        """Register the cucumber on file to the given tank."""
        cuke = Cuke(file)
        return cls.objects.create(
            identifier=file.name.split('/')[-1].rsplit(1)[0],
            tank=tank,
            source_image=file,
            features=cuke.to_dict()
        )
