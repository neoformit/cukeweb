"""Handle requests for image matching against the database."""

from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

from .forms import MatchForm
from .models import MatchSet
from register.models import Tank


def query(request):
    """Interface for user to request image match against database."""
    tanks = Tank.objects.all().values_list("identifier", flat=True)
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            # Run CV model and renders result data to matchset
            match_id = MatchSet.create(form.cleaned_data, request.FILES)
            return redirect('/match/result/?id=%s' % match_id)
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
        matchset = MatchSet.objects.get(identifier=requested_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    return render(
        request,
        'match/result.html',
        matchset.report.request_data()
    )
