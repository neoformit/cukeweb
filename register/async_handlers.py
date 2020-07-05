"""Handlers for AJAX requests."""

import os
import shutil
import pickle as pk
from datetime import datetime

from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.http import HttpResponseBadRequest, HttpResponse


def notify_admin(request):
    """Report a bug in the register app."""
    if not request.method == "POST":
        return HttpResponseBadRequest

    # Collect data
    nowtime = datetime.today().strftime('%Y-%m-%d_%H.%M.%S')
    data = request.session['registration_data']
    filename = request.POST['filename']
    message = request.POST.get('message') or ''  # optional field

    # Set bug report dir and filenames
    fpath = os.path.join(
        settings.MEDIA_ROOT,
        'registration',
        data['tank_id'],
        filename
    )
    report_dir = os.path.join(
        settings.BASE_DIR,
        'cukeweb',
        'logs',
        'bugs',
        '%s_%s' % (nowtime, data['tank_id'])
    )
    new_path = os.path.join(report_dir, filename)
    pkl_path = os.path.join(report_dir, 'report_data.pkl')
    msg_path = os.path.join(report_dir, 'message.txt')

    # Create bug dir and save data to file
    os.mkdir(report_dir)
    shutil.copyfile(fpath, new_path)
    with open(pkl_path, 'wb') as p:
        pk.dump(data, p)
    with open(msg_path, 'w') as f:
        f.write(message)

    # Notify admin
    body = ('A user has submitted a bug report after attempted cucumber'
            ' registration.\n')
    if message:
        body += 'The user submitted the following message:\n'
        body += message
    else:
        body += 'The user did not leave a message.\n'
    body += ('\n\nDetails of this registration have been saved on the web'
             ' server in the following directory:\n%s' % report_dir)
    mail_admins(
        'Bug report on CukeWeb registration',
        body
    )
    return HttpResponse(status=201)
