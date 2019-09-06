from django.contrib.auth import get_user_model

# Note: resolve and reverse are in django.urls in modern versions of Django
from django.core.urlresolvers import resolve, reverse
from django.test import Client, TestCase
from django.utils import timezone

from menu.views import (menu_list, menu_detail, item_detail, create_new_menu,
                        edit_menu)

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

class ViewTestCase(TestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        self.abstract = True
        self.kwargs = {}
        self.name = ''
        self.status_code = 200
        self.target_view = None
        self.template = 'menu/'
        self.url = '/menu/'

        self.client = Client()

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
        print("==== DEBUG ====")
        print("Creating a Simple item:")
        print("---- creating a chef:")
        chef = self.create_valid_user()
        print("...done")
        print("---- creating ingredients:")
        for ingredient in [
            'A bread', 'A lettuce', 'A tomato', 'A bacon',
            'B carrot', 'B coriander', 'B water',
            'C potato', 'C steak', 'C mushrooms',
        ]:
            self.create_valid_ingredient(name=ingredient)
        print("...done")
        print("---- creating item:")
        item = self.create_valid_item(
            chef,
            Ingredient.objects.filter(name__startswith='A'),
            name='BLT'
        )
        print("...done")
        print(item)
        print("==== END DEBUG ====")
        return item


    def create_simple_menu(self):
        print("==== DEBUG ====")
        print("Creating a Simple Menu:")
        print("---- creating a chef:")
        chef = self.create_valid_user()
        print("...done")
        print("---- creating ingredients:")
        for ingredient in [
            'A bread', 'A lettuce', 'A tomato', 'A bacon',
            'B carrot', 'B coriander', 'B water',
            'C potato', 'C steak', 'C mushrooms',
        ]:
            self.create_valid_ingredient(name=ingredient)
        print("...done")
        print("---- creating items:")
        for key, value in {'A': 'BLT', 'B': 'Carrot Soup', 'C': 'Steak Frites'}.items():
            self.create_valid_item(
                chef,
                Ingredient.objects.filter(name__startswith=key),
                name=value
            )
        print("...done")
        print("---- creating menu:")
        menu = self.create_valid_menu(
            Item.objects.all()
        )
        print("...done")
        print(menu)
        print("==== END DEBUG ====")
        return menu

    # Test Methods
    # ------------
    def test_url_resolves_to_correct_view(self):
        """Ensure that expected URLs resolve to their asssociated views"""

        # don't do anything when the method in the base class is called
        if self.abstract:
            return

        resolved_view = resolve(self.url).func

        self.assertEqual(resolved_view, self.target_view)

    def test_view_associated_with_correct_name(self):
        if self.abstract:
            return

        response = self.client.get(
            reverse(self.name, kwargs=self.kwargs)
        )

        self.assertEqual(response.status_code, self.status_code)

    def test_view_renders_correct_template(self):
        if self.abstract:
            return

        response = self.client.get(
            reverse(self.name, kwargs=self.kwargs)
        )

        self.assertTemplateUsed(response, self.template)


class MenuListViewTests(ViewTestCase):
    
    def setUp(self):
        super().setUp()

        self.abstract = False
        self.name += 'menu_list'
        self.target_view = menu_list
        self.template += "list_all_current_menus.html"
        self.url = "/"


class MenuDetailViewTests(ViewTestCase):

    def setUp(self):
        super().setUp()

        self.menu = self.create_simple_menu()

        self.abstract = False
        self.kwargs = {'pk': self.menu.pk}
        self.name += 'menu_detail'
        self.target_view = menu_detail
        self.template += "menu_detail.html"
        self.url += "{}/".format(self.menu.pk)


class ItemDetailViewTests(ViewTestCase):

    def setUp(self):
        super().setUp()

        self.item = self.create_simple_item()

        self.abstract = False
        self.kwargs = {'pk': self.item.pk}
        self.name += 'item_detail'
        self.target_view = item_detail
        self.template += "detail_item.html"
        self.url += "item/{}/".format(self.item.pk)


class CreateNewMenuViewTests(ViewTestCase):

    def setUp(self):
        super().setUp()

        self.abstract = False
        self.name += 'menu_new'
        self.target_view = create_new_menu
        self.template += "menu_edit.html"
        self.url += "new/"


class EditMenuViewTests(ViewTestCase):

    def setUp(self):
        super().setUp()

        self.menu = self.create_simple_menu()

        self.abstract = False
        self.kwargs = {'pk': self.menu.pk}
        self.name += 'menu_edit'
        self.target_view = edit_menu
        self.template += "change_menu.html"
        self.url += "{}/edit/".format(self.menu.pk)
