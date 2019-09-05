import datetime

from django.db import models
from django.utils import timezone


def set_expiry_date():

    now = timezone.now()

    # note, because the timedelta is created with days not years, the future
    # date will not always be exactly two years hence (e.g., if there is a
    # leap year in the interim period).
    # If it became important to be able to express relative time deltas with
    # year units and be precise, we could use the `relativedelta` object
    # from the dateutil package.
    delta = datetime.timedelta(days=(365 * 2))
    future = now + delta
    return future


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')

    # Note: the difference between `auto_now_add=True` and 
    # `default=timezone.now` is that the former disallows manually specifying
    # a value (i.e., it can *only* be 'now'); the latter merely makes 'now'
    # the default, but can be manually overridden.
    created_date = models.DateTimeField(auto_now_add=True)

    # We don't want to allow blank/null expiration dates as the application
    # is designed to be able to perform comparisons on expiration_date values.
    # We'll set a reasonable default of 2 years from now
    expiration_date = models.DateTimeField(default=set_expiry_date)

    class Meta:
        ordering = ['expiration_date', 'season']

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(auto_now_add=True)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
