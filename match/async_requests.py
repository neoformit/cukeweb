"""Handle asynchronous requests for image matching."""

from django.http import JsonResponse, HttpResponseBadRequest
from register.models import Tank, Cucumber


def fetch_cuke_ids(request):
    """Fetch all cuke identifiers assigned to the given tank."""
    if request.method != "POST":
        return HttpResponseBadRequest
    tank = Tank.objects.get(identifier__iexact=request.POST['tank_id'])
    cuke_ids = Cucumber.objects.filter(
        tank=tank).values_list('identifier', flat=True)
    return JsonResponse({'identifiers': list(cuke_ids)})
