"""Management interface for Tanks, Cucumbers and MatchResults."""

from django.shortcuts import render
from register.models import Tank


def manage(request):
    """Page for user to view and manage tanks and cucumbers."""
    return render(request, 'manager/home.html', {
        'tanks': Tank.render_status()
    })
