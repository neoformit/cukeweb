"""Cukeweb homepage forms."""

from django import forms
from django.contrib import auth     # login, logout, authenticate
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """Validate and process user login."""

    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        """Pass request to form instance."""
        if "request" in kwargs:
            self.request = kwargs.pop("request")
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Assert valid username and password."""
        data = self.cleaned_data
        self.user = auth.authenticate(
            self.request,
            username=data['username'],
            password=data['password']
        )
        if self.user is None:
            raise ValidationError({'password': 'Invalid login credentials'})
        return data

    def login(self):
        """Log in authenticated user."""
        auth.login(self.request, self.user)
