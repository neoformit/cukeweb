"""Return a static homepage as the site index."""

from django.shortcuts import render


def home(request):
    """Render a static homepage."""
    return render(request, 'home/index.html')


def info(request):
    """Render a static information page."""
    return render(request, 'home/information.html')
