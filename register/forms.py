from django import forms
from .models import


class RegistrationForm(forms.Form):
    """For users to register Cucumbers with a new or existing Tank."""

    tank_id = forms.CharField(max_length=25)
    images = forms.FileField()
