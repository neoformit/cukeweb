"""Take report data from session and render as PDF for download/browser."""

import os
import subprocess
from django.conf import settings
from django.template.loader import render_to_string

from .models import MatchRecord

import logging
logger = logging.getLogger('django')


def render(request, result_id):
    """Render to html template and convert to PDF."""
    data = MatchRecord.objects.get(identifier=result_id).render(tex=True)
    filename = 'report_%s.pdf' % data['result_id']
    tex_fname = filename.replace('.pdf', '.tex')
    tex_dir = os.path.join(
        settings.MEDIA_ROOT,
        'temp',
        'latex'
    )
    tex_path = os.path.join(tex_dir, tex_fname)
    report_uri = os.path.join(
        settings.MEDIA_URL,
        'temp',
        'latex',
        tex_fname.replace('.tex', '.pdf')
    )

    # Render tex file from report template
    tex = render_to_string('match/report.tex', data)
    with open(tex_path, 'w') as f:
        f.write(tex)

    # Render tex file to pdf
    subprocess.run([
        'pdflatex',
        '-output-directory', tex_dir,
        tex_fname,
    ])

    return report_uri
