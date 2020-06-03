"""Take report data from session and render as PDF for download/browser."""

import os
import pdfkit
from django.conf import settings
from django.template.loader import render_to_string


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
    pdfkit.from_string(
        render_to_string('register/report.html', data),
        report_path
    )
    return report_uri
