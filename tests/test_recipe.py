from django.test import TestCase
from django.contrib.auth.models import User
from core.models.Recipe import Recipe
from recipes.models.Category import Category

class RecipeModelTest(TestCase):

    def test_create_recipe(self):
        user = User.objects.create_user(username='lorena', password='12345')

        category = Category.objects.create(
            name='Postres',
            user_id=user  
        )

        recipe = Recipe.objects.create(
            name='Tarta de manzana',
            description='Receta de la abuela',
            user_id=user,
            category_id=category,
            duration_minutes=45,
            commensals=4,
        )

        self.assertIsNotNone(recipe.id)
        self.assertEqual(recipe.name, 'Tarta de manzana')
        self.assertEqual(recipe.user_id.username, 'lorena')
        self.assertEqual(recipe.category_id.name, 'Postres')
        self.assertEqual(recipe.duration_minutes, 45)
        self.assertEqual(recipe.commensals, 4)
