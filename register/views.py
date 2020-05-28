"""Views for registering new cucumbers and creating new tanks."""

from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from .models import Tank
from .forms import RegistrationForm
from .register import register_cuke


def register(request):
    """Register new cucumbers to a tank."""
    tank_ids = Tank.objects.all().values_list('identifier', flat=True)
    return render(request, 'register/register.html', {'tanks': tank_ids})


def confirm(request):
    """Confirm that animals were successfully registered."""
    def get_or_create_tank(tank_id):
        """Return tank instance to register cucumbers to."""
        try:
            return Tank.objects.get(identifier=tank_id)
        except ObjectDoesNotExist:
            return Tank.objects.create(identifier=tank_id)

    if request.method != 'POST':
        return HttpResponseBadRequest()

    form = RegistrationForm(request.POST)
    files = request.FILES.getlist('images')
    if form.is_valid():
        tank_id = form.cleaned_data['tank_id']
        tank = get_or_create_tank(tank_id)
        for file in files:
            # Save as serialized cuke instance
            register_cuke(file, tank)
        return render(request, 'register/confirm.html')
    # Else we should define some response to failed validation
