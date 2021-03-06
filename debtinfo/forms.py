from .models import *
from django import forms


class SearchForm(forms.Form):
    """Configure and return a search form."""

    q = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'validate'}))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].label = 'Search'
