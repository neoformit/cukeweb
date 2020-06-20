"""Take report data from session and render as PDF for download/browser."""

import os
import pdfkit
from django.conf import settings
from django.template.loader import render_to_string

import logging
logger = logging.getLogger('django')


def render(request):
    """Render to html template and convert to PDF."""
    data = request.session['registration_data']
    filename = 'report_%s.pdf' % data['identifier']
    report_path = os.path.join(
        settings.MEDIA_ROOT,
        'temp',
        'reports',
        filename
    )
    report_uri = os.path.join(
        settings.MEDIA_URL,
        'temp',
        'reports',
        filename
    )
    sections = len(data['registered'] + data['failed'])
    page_height = round(sections * 2.2)
    logger.info("Printing to pdf with page height %scm" % page_height)

    config = pdfkit.configuration(
        wkhtmltopdf=bytes('/usr/bin/wkhtmltopdf', 'utf-8')
    )
    pdfkit.from_string(
        render_to_string('register/report.html', data),
        report_path,
        options={
            'disable-local-file-access': None,
            'allow': '/srv/sites/cukeweb/cukeweb/media/',
        },
        configuration=config,
    )
    return report_uri
