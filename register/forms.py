from django import forms


class RegistrationForm(forms.Form):
    """For users to register Cucumbers with a new or existing Tank."""

    tank_id = forms.CharField(max_length=25)
    images = forms.FileField()
    infer_id = forms.BooleanField(required=False)
    id_prefix = forms.CharField(max_length=10, required=False)
