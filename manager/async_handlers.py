"""Handlers for AJAX requests."""

import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from register.models import Tank, Cucumber


def delete_tank(request):
    """Delete tank instance defined in request."""
    if not request.method == "POST":
        return HttpResponseBadRequest
    Tank.objects.get(identifier=request.POST['tank_id']).delete()
    return HttpResponse(status=200)


def delete_cuke(request):
    """Delete cucumber instance defined in request."""
    if not request.method == "POST":
        return HttpResponseBadRequest
    tank = Tank.objects.get(identifier=request.POST['tank_id'])
    Cucumber.objects.get(
        tank=tank,
        identifier=request.POST['cuke_id'],
    ).delete()
    return HttpResponse(status=200)


def update_cuke(request):
    """Delete tank instance defined in request."""
    if not request.method == "POST":
        return HttpResponseBadRequest
    tank = Tank.objects.get(identifier=request.POST['tank_id'])
    cuke = Cucumber.objects.get(tank=tank, identifier=request.POST['cuke_id'])
    updated = {}

    for k, v in json.loads(request.POST['details']).items():
        if v is None:
            # Field was deleted
            cuke.details.pop(k)
            updated[k] = None
            continue
        if k != v['key']:
            # Key was updated
            cuke.details.pop(k)
        # Update field with new value
        updated[k] = [v['key'].capitalize(), v['value']]
        cuke.details[v['key'].capitalize()] = v['value']

    cuke.save()
    return JsonResponse(updated)
