import datetime

from django.db import models
from django.utils import timezone


def set_expiry_date():
    now = datetime.datetime.now()
    naive_future = datetime.datetime(now.year + 2, now.month, now.day)
    aware_future = timezone.make_aware(naive_future, is_dst=True)
    return aware_future


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(auto_now_add=True)

    # We don't want to allow blank/null expiration dates as the application
    # is designed to be able to perform comparisons on expiration_date values.
    # We'll set a reasonable default of 2 years from now
    expiration_date = models.DateTimeField(default=set_expiry_date)

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
