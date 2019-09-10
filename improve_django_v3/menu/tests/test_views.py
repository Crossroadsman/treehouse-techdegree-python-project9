import datetime

# Note: resolve and reverse are in django.urls in modern versions of Django
from django.core.urlresolvers import resolve, reverse
from django.test import Client
from django.utils import timezone

from menu.views import (menu_list, menu_detail, item_detail, create_new_menu,
                        edit_menu)

from menu.models import Ingredient, Item, Menu

from .base import MenuTestCase


class ViewTestCase(MenuTestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()

        self.kwargs = {}
        self.name = ''
        self.status_code = 200
        self.target_view = None
        self.template = 'menu/'
        self.url = '/menu/'

        self.client = Client()
    
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

    def test_redirects_to_menu_detail_on_valid_POST(self):
        """Note: this test also implicitly tests that a valid post
        creates a valid db model, since we need to fetch that model
        to get the PK to build the redirect path
        """
        self.create_simple_menu()  # creates the associated models we need

        # create data for POSTing
        postdata = {
            'season': 'test season 2019',
            'items': [1, 2, 3],  # these are the pks of the items created above
            'expiration_date': "2020-01-31 13:45:01"
        }

        response = self.client.post(
            reverse(self.name),
            data=postdata
        )

        menu_pk = Menu.objects.get(season='test season 2019').pk
        expected_redirect_target = '/menu/{}/'.format(menu_pk)

        self.assertRedirects(response, expected_redirect_target)


class EditMenuViewTests(ViewTestCase):

    def setUp(self):
        super().setUp()
        
        # creates the associated models we need
        self.menu = self.create_simple_menu()

        self.abstract = False
        self.kwargs = {'pk': self.menu.pk}
        self.name += 'menu_edit'
        self.target_view = edit_menu
        self.template += "change_menu.html"
        self.url += "{}/edit/".format(self.menu.pk)

    def test_updates_db_on_valid_POST(self):

        # create data for POSTing
        postdata = {
            'season': 'test season 2019',
            'items': [2, 3],  # these are the pks of the items created above
            'expiration_date': "2020-01-31 13:45:01"
        }

        self.client.post(
            reverse(self.name, kwargs=self.kwargs),
            data=postdata
        )

        # this line will fail if the test fails
        Menu.objects.get(season='test season 2019').pk
