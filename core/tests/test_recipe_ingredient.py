from django.test import TestCase
from models.Recipe import Recipe
from models.Ingredient import Ingredient
from models.RecipeIngredient import RecipeIngredient



class RecipeIngredientModelTest(TestCase):

    def setUp(self):
        # Crear receta de prueba
        self.recipe = Recipe.objects.create(name="Tortilla", description="Tortilla de patatas")
        
        # Crear ingrediente de prueba
        self.ingredient = Ingredient.objects.create(name="Huevos", description="Huevos frescos")

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


