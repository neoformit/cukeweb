"""Signals define various hooks which perform a function on a given event.

Events include pre_save, post_save, pre_delete, post_delete.

Typical usage might be deleting files associated with a model instance using a
post_delete hook or modifying the model instance attributes before saving with
a pre_save hook.

Signals may be fired in duplicate in testing, so it is best to guard them
against double-firing (e.g. check if file exists before creating).
"""

import os
import shutil
import logging

from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from django.conf import settings

from .models import Tank, Cucumber

logger = logging.getLogger('django')


@receiver(post_delete, sender=Tank)
def remove_tank_files(sender, instance, using, **kwargs):
    """Remove image files linked to model instance."""
    logger.info('Tank deleted - removing registered image files.')
    dpath = os.path.join(
        settings.BASE_DIR,
        'cukeweb',
        'media',
        'registration',
        instance.identifier
    )
    try:
        shutil.rmtree(dpath)
    except Exception as exc:
        logger.error("Error removing Tank image file:\n%s" % str(exc))


@receiver(post_delete, sender=Cucumber)
def remove_cuke_files(sender, instance, using, **kwargs):
    """Remove image files linked to model instance."""
    logger.info('Cucumber deleted - removing registered image file.')
    try:
        os.remove(instance.source_image.path)
    except Exception as exc:
        logger.error("Error removing Cucumber image file:\n%s" % str(exc))
