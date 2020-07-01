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

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings

from .models import MatchRecord
from utilities.disk import check_disk_space

logger = logging.getLogger('django')


@receiver(post_delete, sender=MatchRecord)
def remove_match_files(sender, instance, using, **kwargs):
    """Remove image files linked to model instance."""
    # This is the place where images may potentially accumulate and swallow
    # disk space. Best to check and report if disk is getting full.
    check_disk_space()

    dpath = os.path.join(
        settings.BASE_DIR,
        'cukeweb',
        'media',
        'match',
        instance.identifier
    )
    try:
        shutil.rmtree(dpath)
    except Exception as exc:
        logger.error("Error removing MatchRecord directory:\n%s" % str(exc))
