"""Handle requests for image matching against the database."""

import pprint

from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

from .forms import MatchForm
from .models import MatchRecord
from register.models import Tank

import logging
logger = logging.getLogger('django')


def query(request):
    """Interface for user to request image match against database."""
    tank_ids = set(Tank.objects.filter(  # Only tanks containing cukes
        cucumber__identifier__isnull=False).values_list(
            "identifier", flat=True))
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
            "tanks": tank_ids
        })
    # Assume GET
    if not tank_ids:
        return no_occupied_tanks(request)

    form = MatchForm()
    return render(request, 'match/match.html', {
        "form": form,
        "tanks": tank_ids
    })


def no_occupied_tanks(request):
    """User requested the match app with no cukes registered."""
    return render(request, 'match/no-cukes.html')


def result(request):
    """Retrieve match results and render to results interface."""
    requested_id = request.GET.get('id')
    try:
        matchset = MatchRecord.objects.get(identifier=requested_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    return render(request, 'match/result.html', matchset.render())


def colors(request):
    """View to play with score color scale."""
    def color_scale(x):
        g = round(200 * (x / 1000))
        r = round(100 - g / 2)
        b = 30
        return "rgb(%s,%s,%s,0.75)" % (r, g, b)

    colors = [(i, color_scale(i)) for i in range(0, 1000, 50)]
    return render(request, 'match/colors.html', {'colors': colors})
