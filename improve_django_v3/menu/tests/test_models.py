import datetime

from .base import MenuTestCase, VALID_INGREDIENT_DATA

from menu.models import Menu, Item, Ingredient


class MenuModelTests(MenuTestCase):
    
    # Setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()

        self.create_simple_menu()
        self.test_menu = Menu.objects.get(season='fall 2019')

    # Tests
    # -----
    def test_create_model_database_has_correct_data(self):
        expected_items = {'BLT', 'Carrot Soup', 'Steak Frites'}
        test_items = set(self.test_menu.items.values_list('name', flat=True))

        self.assertEqual('fall 2019', self.test_menu.season)
        self.assertEqual(expected_items, test_items)

    def test_create_expiration_date_is_correctly_generated(self):
        created_date = self.test_menu.created_date
        expected_expiry = created_date + datetime.timedelta(days=(365 * 2))

        almost_equal_delta = datetime.timedelta(seconds=10)

        self.assertAlmostEqual(
            expected_expiry,
            self.test_menu.expiration_date,
            delta=almost_equal_delta
        )

    def test_meta_models_are_correctly_ordered(self):
        items = self.test_menu.items.all()
        self.create_valid_menu(
            items=items,
            season='early 2020',
        )
        test_menu_3 = self.create_valid_menu(
            items=items,
            season='beginning 2018',
        )
        test_menu_3.expiration_date = self.test_menu.expiration_date
        test_menu_3.save()

        # first: beginning 2018 (same expiry as fall 2019 but season comes
        #        first alphanetically);
        # second: fall 2019
        # third: early 2020 (expiration date comes after the other two)
        expected_order = ['beginning 2018', 'fall 2019', 'early 2020']

        results = list(Menu.objects.all().values_list('season', flat=True))

        self.assertEqual(expected_order, results)


class ItemModelTests(MenuTestCase):
    # Setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()

        self.create_simple_item()
        self.test_item = Item.objects.get(name='BLT')

    # Tests
    # -----
    def test_create_model_database_has_correct_data(self):
        expected_ingredients = {'A bread', 'A lettuce', 'A tomato', 'A bacon'}
        test_ingredients = set(self.test_item.ingredients.values_list('name', flat=True))

        self.assertEqual('BLT', self.test_item.name)
        self.assertEqual('A delicious sandwich', self.test_item.description)
        self.assertEqual('swedish chef', self.test_item.chef.username)
        self.assertEqual(expected_ingredients, test_ingredients)



class IngredientModelTests(MenuTestCase):
    
    # Setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()

        self.test_model_data = VALID_INGREDIENT_DATA
        self.create_valid_ingredient()
        self.test_ingredient = Ingredient.objects.get(name=self.test_model_data['name'])

    # Tests
    # -----
    def test_create_model_correctly_reflects_data(self):
        for key, value in self.test_model_data.items():
            self.assertEqual(
                value,
                getattr(self.test_ingredient, key)
            )

    def test_create_saves_valid_model_to_db(self):
        db_model = Ingredient.objects.get(name=self.test_ingredient.name)

        self.assertEqual(
            db_model,
            self.test_ingredient
        )

