"""Return a static homepage as the site index."""

from django.contrib import auth
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from .forms import LoginForm

User = get_user_model()


def home(request):
    """Render a static homepage. Defaults to login page."""
    if not request.user.is_authenticated:
        return login(request)
    return render(request, 'home/index.html')


def info(request):
    """Render a static information page."""
    video_url = settings.MEDIA_URL + "tutorial.mp4"
    return render(request, 'home/information.html', {'video_url': video_url})


def login(request):
    """Display and process user login."""
    if request.method == "POST":
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            form.login()
            return redirect('/')

        # Return an 'invalid login' error message.
        return render(request, 'home/login.html', {
            'form': form
        })

    # Assume GET request
    form = LoginForm()
    return render(request, 'home/login.html', {
        'form': form
    })


def logout(request):
    """Log user out and return to login screen."""
    auth.logout(request)
    return redirect('/')
