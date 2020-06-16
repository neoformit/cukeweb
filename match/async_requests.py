"""Handle asynchronous requests for image matching."""

from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
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


def email_result_link(request):
    """Email results page link to the given email address."""
    if request.method != "POST":
        return HttpResponseBadRequest
    address = request.POST['address']
    match_url = (settings.BASE_URL
                 + 'match/result/?id=%s' % request.POST['match_id'])
    subject = "Match result from The Cuke Register"
    body = 'View your recent image match result here:\n' + match_url
    send_mail(subject, body, settings.DEFAULT_EMAIL, [address])
    return HttpResponse(status=200)
