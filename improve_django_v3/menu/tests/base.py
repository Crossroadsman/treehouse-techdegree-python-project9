from django.contrib.auth import get_user_model
from django.test import TestCase

from menu.models import Ingredient, Item, Menu


User = get_user_model()


VALID_INGREDIENT_DATA = {
    'name': 'carrot',
}
VALID_USER_DATA = {
    'username': 'swedish chef'
}
VALID_ITEM_DATA = {
    'name': 'carrot soup',
    'description': 'a soup that is mostly carrot',
    # chef
    # ingredients
}
VALID_MENU_DATA = {
    'season': 'fall 2019',
    # items
}


class MenuTestCase(TestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):

        self.abstract = True

    # Helper Methods
    # --------------
    def create_valid_ingredient(self, **kwargs):
        ingredient = Ingredient(**VALID_INGREDIENT_DATA)
        for key, value in kwargs.items():
            setattr(ingredient, key, value)
        ingredient.save()
        return ingredient

    def create_valid_user(self, **kwargs):
        user = User(**VALID_USER_DATA)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user

    def create_valid_item(self, chef, ingredients, **kwargs):
        """chef is a User object, ingredients is a queryset of Ingredient
        objects or a list of ingredient PKs
        """
        valid_data = {**VALID_ITEM_DATA, 'chef': chef}
        item = Item(**valid_data)
        for key, value in kwargs.items():
            setattr(item, key, value)
        item.save()  # can't add MTM relations to an object that isn't in DB
        item.ingredients = ingredients
        item.save()
        return item

    def create_valid_menu(self, items, **kwargs):
        """items is a non-empty queryset of Item objects or a
        list of item PKs
        """
        menu = Menu(**VALID_MENU_DATA)
        for key, value in kwargs.items():
            setattr(menu, key, value)
        menu.save()  # can't add MTM relations to an object that isn't in DB
        menu.items = items
        menu.save()
        return menu

    def create_simple_item(self):
        chef = self.create_valid_user()
        for ingredient in [
            'A bread', 'A lettuce', 'A tomato', 'A bacon',
            'B carrot', 'B coriander', 'B water',
            'C potato', 'C steak', 'C mushrooms',
        ]:
            self.create_valid_ingredient(name=ingredient)

        item = self.create_valid_item(
            chef,
            Ingredient.objects.filter(name__startswith='A'),
            name='BLT',
            description='A delicious sandwich'
        )
        return item

    def create_simple_menu(self):
        chef = self.create_valid_user()
        for ingredient in [
            'A bread', 'A lettuce', 'A tomato', 'A bacon',
            'B carrot', 'B coriander', 'B water',
            'C potato', 'C steak', 'C mushrooms',
        ]:
            self.create_valid_ingredient(name=ingredient)
        for key, value in {
            'A': 'BLT', 'B': 'Carrot Soup', 'C': 'Steak Frites'
        }.items():
            self.create_valid_item(
                chef,
                Ingredient.objects.filter(name__startswith=key),
                name=value
            )
        menu = self.create_valid_menu(
            Item.objects.all()
        )
        return menu
