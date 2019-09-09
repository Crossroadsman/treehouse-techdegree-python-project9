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
        pass

    def test_meta_models_are_correctly_ordered(self):
        pass


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

