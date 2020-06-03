"""Views for registering new cucumbers and creating new tanks."""

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from . import uploads, pdf
from .models import Tank
from .forms import RegistrationForm


def register(request):
    """Register new cucumbers to a tank."""
    def get_or_create_tank(tank_id):
        """Return tank instance to register cucumbers to."""
        try:
            return Tank.objects.get(identifier=tank_id)
        except ObjectDoesNotExist:
            return Tank.objects.create(identifier=tank_id)

    tank_ids = Tank.objects.all().values_list('identifier', flat=True)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            tank = get_or_create_tank(form.cleaned_data['tank_id'])
            report = uploads.register(request.FILES, tank)
            # Session data for access by pdf.render
            request.session['registration_data'] = report.report_data()
            return render(request, 'register/confirm.html',
                          report.request_data())

        # Problem with form - unusual as js validation in frontend
        return render(request, 'register/register.html', {
            'tanks': tank_ids,
            'error_msg': form.errors
        })

    # assume GET
    return render(request, 'register/register.html', {'tanks': tank_ids})


def report(request):
    """Generate a PDF report for user's most recent registration."""
    uri = pdf.render(request)
    return redirect(uri)
