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

        # This will be a tz-aware datetime object, the timezone is assumed to
        # be the timezone specified in settings.TIME_ZONE
        # This might cause confusion if this application is used outside
        # California. For a production-ready version of this app we could
        # have a user-specific timezone associated with the user's profile
        # and then build the datetime object from the user's supplied
        # date/time values but assuming the user's profile tz offset instead
        # of the server's.
        # This is beyond the scope of the next project milestone
        expiration_date = self.cleaned_data.get('expiration_date')

        now = timezone.now()
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

        error_messages = {
            'items': {
                'required': 'A valid menu must have at least one item'
            },
            'season': {
                'required': 'The season must be specified'
            }
        }
