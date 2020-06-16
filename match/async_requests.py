"""Handle asynchronous requests for image matching."""

from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseBadRequest

from .models import MatchRecord, Match
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
    result_url = (settings.BASE_URL
                  + 'match/result/?id=%s' % request.POST['result_id'])
    subject = "Match result from The Cuke Register"
    body = 'View your recent image match result here:\n' + result_url
    send_mail(subject, body, settings.DEFAULT_EMAIL, [address])
    return HttpResponse(status=200)


def reject_match(request):
    """Fetch the next-best match from the specified Match instance."""
    if request.method != "POST":
        return HttpResponseBadRequest
    result = MatchRecord.objects.get(identifier=request.POST['result_id'])
    match = Match.objects.get(
        record=result, identifier=request.POST['match_id'])
    try:
        if request.POST['undo'] == 'true':
            return JsonResponse(match.fetch_previous_match())
        return JsonResponse(match.fetch_next_match())
    except IndexError:
        return JsonResponse({'error': 'No more matches to fetch'})
