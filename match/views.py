"""Handle requests for image matching against the database."""

import pprint

from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

from .forms import MatchForm
from .models import MatchRecord
from register.models import Tank

import logging
logger = logging.getLogger('main')


def query(request):
    """Interface for user to request image match against database."""
    tanks = Tank.objects.all().values_list("identifier", flat=True)
    if request.method == "POST":
        form = MatchForm(request.POST, request.FILES)
        if form.is_valid():
            # Run CV model and render result data to match report
            logger.info("Match form validated."
                        " Rendering images to Match instances...")
            match_id = MatchRecord.create(form.cleaned_data, request.FILES)
            return redirect('/match/result/?id=%s' % match_id)
        # Form not validated
        logger.error("MatchForm errors: %s" % pprint.pformat(form.errors))
        return render(request, 'match/match.html', {
            "form": form,
            "tanks": tanks
        })
    # Assume GET
    form = MatchForm()
    return render(request, 'match/match.html', {
        "form": form,
        "tanks": tanks
    })


def result(request):
    """Retrieve match results and render to results interface."""
    requested_id = request.GET.get('id')
    try:
        matchset = MatchRecord.objects.get(identifier=requested_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    return render(request, 'match/result.html', matchset.render())
