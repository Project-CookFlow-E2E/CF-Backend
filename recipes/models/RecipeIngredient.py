from django.db import models
from recipes.models.recipe import Recipe
from recipes.models.ingredient import Ingredient


class RecipeIngredient(models.Model):
    """
    Modelo de RecipeIngredient, representa los ingredientes de una receta con su cantidad y unidad.

    Args:
        models (Model): Clase base de Django para modelos.
    Attributes:
        recipe_id (BigInteger): ID de la receta, clave foránea relacionada con Recipe.
        ingredient_id (BigInteger): ID del ingrediente, clave foránea relacionada con Ingredient.
        quantity (Integer): Cantidad del ingrediente.
        unit (str): Unidad de medida (máx. 50 caracteres).
        created_at (DateTimeField): Fecha de creación, se establece automáticamente.
    
    Author:
        {Rafael Fernández}
    """
       
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_recipes")
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Metadatos del modelo RecipeIngredient.
        Define el nombre exacto de la tabla en la base de datos.
        """
        db_table = 'recipe_ingredients'
