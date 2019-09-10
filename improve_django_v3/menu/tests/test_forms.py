import datetime

from django.utils import timezone

from .base import MenuTestCase
from menu.forms import MenuForm


class MenuFormTests(MenuTestCase):

    # Setup and Teardown
    # ------------------
    def setUp(self):
        self.required_form_fields = [
            'season',
            'items',
            'expiration_date'
        ]

        self.valid_menu = self.create_simple_menu()
        # We want a list of PKs as strings to instantiate the items relation
        # in the form
        self.items = [
            str(x) for x in self.valid_menu.items.all().values_list(
                'pk', flat=True
            )
        ]

    # Tests
    # -----
    def test_form_renders_inputs(self):
        form = MenuForm()
        expected_inputs = self.required_form_fields

        rendered_form = form.as_p()

        for field in expected_inputs:
            self.assertIn('id_{}'.format(field), rendered_form)

    def test_form_fails_validation_if_required_item_missing(self):
        season = self.valid_menu.season
        expiration_date = self.valid_menu.expiration_date

        no_season_form = MenuForm(
            data={
                'items': self.items,
                'expiration_date': expiration_date
            }
        )
        no_items_form = MenuForm(
            data={
                'season': season,
                'expiration_date': expiration_date
            }
        )
        no_expirationdate_form = MenuForm(
            data={
                'season': season,
                'items': self.items
            }
        )

        for form in [no_season_form, no_items_form, no_expirationdate_form]:
            self.assertFalse(form.is_valid())

    def test_valid_formdata_passes_validation(self):
        # a valid season has at least 2 characters
        # a valid expiration date is later than now
        form = MenuForm(
            data={
                'season': self.valid_menu.season,
                'items': self.items,
                'expiration_date': self.valid_menu.expiration_date
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_season_fails_validation(self):
        form = MenuForm(
            data={
                'season': 'a',
                'items': self.items,
                'expiration_date': self.valid_menu.expiration_date
            }
        )

        self.assertFalse(form.is_valid())

    def test_invalid_expiration_date_fails_validation(self):
        now = timezone.now()
        timedelta = datetime.timedelta(seconds=1)
        invalid_expiration_date = now - timedelta

        form = MenuForm(
            data={
                'season': self.valid_menu.season,
                'items': self.items,
                'expiration_date': invalid_expiration_date
            }
        )

        self.assertFalse(form.is_valid())
