from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models.Recipe import Recipe
from core.models.Ingredient import Ingredient
from core.models.RecipeIngredient import RecipeIngredient

User = get_user_model()

class RecipeIngredientModelTest(TestCase):

    def setUp(self):
        # Crear usuario obligatorio para la receta
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

        # Crear receta de prueba con todos los campos obligatorios
        self.recipe = Recipe.objects.create(
            name="Tortilla",
            description="Tortilla de patatas",
            duration_minutes=30,
            commensals=2,
            user=self.user  # Campo obligatorio
        )

        # Crear ingrediente de prueba
        self.ingredient = Ingredient.objects.create(
            name="Huevos",
            description="Huevos frescos"
        )

    def test_create_recipe_ingredient(self):
        # Crear relación de receta con ingrediente
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=3,
            unit="unidades"
        )

        self.assertEqual(recipe_ingredient.recipe, self.recipe)
        self.assertEqual(recipe_ingredient.ingredient, self.ingredient)
        self.assertEqual(recipe_ingredient.quantity, 3)
        self.assertEqual(recipe_ingredient.unit, "unidades")
