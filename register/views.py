"""Views for registering new cucumbers and creating new tanks."""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from . import uploads
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
            tank_id = form.cleaned_data['tank_id']
            tank = get_or_create_tank(tank_id)
            success_count, invalid = uploads.register(request.FILES, tank)
            return render(request, 'register/confirm.html',
                          {'count': success_count, 'invalid': invalid})
        # Problem with form
        return render(request, 'register/register.html', {
            'tanks': tank_ids,
            'error_msg': form.errors
        })

    # assume GET
    return render(request, 'register/register.html', {'tanks': tank_ids})
