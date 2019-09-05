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

    # It's not entirely clear what the 'season' field is intended for.
    # The short `max_length=20` in the original code suggests that this field
    # was intended to reference a relatively small number of possible
    # seasons, in which case it would seem better as a FK relation to a 
    # dedicated Season object (FK not MTM because a seasonal menu 'belongs' to 
    # a particular season, but a season might have multiple menus (e.g., a 
    # drinks menu, a dessert menu, etc)).
    # Alternatively, the actual data provided has many menus with totally
    # unique string values (as distinct from lots of similar or identical 
    # string values). This might suggest that the season field is being used
    # not as a way of tying the menu to a particular season, but simply as a
    # name for the menu. If the intent is to use this as a name for the menu
    # (note there is no other attribute on the model that could be the menu's
    # name) then we would want to keep this as a CharField but allow a longer
    # string and make this field unique.
    # Without any guidance beyond the code and the provided data we have to
    # guess as to what the proper intent is for this field.
    # If the supplied data looked like it was hand-coded, we could infer from
    # the values themselves what the actual usage ought to be. Unfortunately,
    # the values are just a load of randomly-generated lorem ipsum code that
    # offers no clues about the real intent of this field. However, the sheer
    # number of values (504) hints that season is just a name and not a 
    # reference to a time of year.
    # Thus we will configure the field as follows:
    # - leave the fieldname as `season`: although this fieldname is ambiguous
    #   and thus not ideal, it was clearly chosen for a reason, perhaps there
    #   is some domain-specific knowledge that we lack about restaurant menus 
    #   that informs this fieldname choice, so we will leave it as-is.
    # - leave the field as a CharField: since this is the name of the menu and
    #   not a reference to another 'thing', it doesn't make sense for this
    #   field to be a relation to another object. Names can be quite long, but
    #   not arbitrarily so, thus CharField is a better choice than TextField
    # - make max_length=200: The other objects in this project allow names up
    #   to 200 characters. 20 is very limiting and hints that at some time in
    #   this project's history, it was expected that season would be a 
    #   reference to a season (e.g., 'fall') rather than a name 
    #   (e.g., 'Fall 2018 Dinner Menu' or 'Appetizers and Shareables'). Having
    #   concluded that actual use deviates from the earliest design 
    #   expectations, we are increasing the max_length to correspond to 
    #   expected usage.
    # - make unique=True: In order for this field to be useful as a name, it
    #   must uniquely identify the menu.
    season = models.CharField(max_length=200, unique=True)
    
    items = models.ManyToManyField('Item', related_name='items')

    # Note: the difference between `auto_now_add=True` and 
    # `default=timezone.now` is that the former disallows manually specifying
    # a value (i.e., it can *only* be 'now'); the latter merely makes 'now'
    # the default, but can be manually overridden.
    created_date = models.DateTimeField(auto_now_add=True)

    # We don't want to allow blank/null expiration dates as the application
    # is designed to be able to perform comparisons on expiration_date values.
    # We'll set a reasonable default of 2 years from the creation_date
    expiration_date = models.DateTimeField(default=set_expiry_date)

    class Meta:
        ordering = ['expiration_date', 'season']

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(auto_now_add=True)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
