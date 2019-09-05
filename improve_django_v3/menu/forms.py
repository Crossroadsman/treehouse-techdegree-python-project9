from datetime import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone

from .models import Menu, Item, Ingredient


class MenuForm(forms.ModelForm):

    # Note: method declarations for cleaning must come before the
    # Meta class declaration
    def clean_season(self):
        season = self.cleaned_data.get('season')
        if len(season) < 2:
            raise forms.ValidationError("Season must be at least 2 characters")
        return season

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')


        # TODO: NEED TO MAKE SURE THIS HANDLES ALL COMBINATIONS OF
        # CLIENT/SERVER TIMEZONE.
        # WE MIGHT BE ABLE TO DO THE SAME AS WE DID IN THE MODEL
        # HOW DO WE KNOW WHAT THE CLIENT TIMEZONE IS, OR IS IT ALWAYS 
        # THE SERVER'S TIMEZONE?
        now = datetime.datetime.now()
        if expiration_date < now:
            raise forms.ValidationError("expiration date must be in the future")
        return expiration_date

    class Meta:
        model = Menu

        fields = (
            "season",
            "items",
            "expiration_date",
        )
