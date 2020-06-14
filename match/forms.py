"""Forms for submitting an image match request."""

from django import forms


class MatchForm(forms.Form):
    """Take input parameters to perform an image match."""

    tank_id = forms.CharField(max_length=25)
    target_ids = forms.CharField()
    images = forms.ImageField()

    def clean(self):
        """Validate and clean form data."""
        data = self.cleaned_data
        data['target_ids'] = data['target_ids'].split('|')
        return data
