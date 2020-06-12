"""Handle requests for image matching against the database."""

from django.shortcuts import render, redirect

import match
from .forms import MatchForm
from register.models import Tank


def query(request):
    """Interface for user to request image match against database."""
    tanks = Tank.objects.all().values_list("identifier", flat=True)
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            match_id = match.make(form.cleaned_data)
            matchset = form.save()
            match.make(matchset)
            return redirect('/match/result/?id=%s' % match_id)
        else:
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
    return None
