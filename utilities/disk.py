"""Utilities for managing disk space."""

from shutil import disk_usage
from django.core.mail import mail_admins


def check_disk_space():
    """Check disk space and report if too full."""
    du = disk_usage('/')
    gb_free = du.free / 1000000000
    if gb_free < 2:
        mail_admins(
            'Cukeweb disk usage alert',
            ('There is only 2GB of disk space left on the cukeweb server.'
             ' Please check temp image files in cukeweb/cukeweb/media'
             ' directory and delete files as necessary.'),
        )
