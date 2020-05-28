"""Return a static homepage as the site index."""

from django.shortcuts import render


def home(request):
    """Render a  static homepage."""
    return render(request, 'home/index.html')
