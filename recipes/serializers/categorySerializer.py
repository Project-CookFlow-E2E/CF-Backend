from rest_framework import serializers
from recipes.models.category import Category
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from recipes.serializers.recipeSerializer import RecipeSerializer
from recipes.serializers.ingredientSerializer import IngredientSerializer
from django.db import models


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer de Category, representa las diferentes categorías asociadas a recetas e ingredientes.

    Args:
        serializers.ModelSerializer: Clase base de DRF para serializers basados en modelos.

    Attributes:
        `id (int)`: Identificador único de la categoría.
        `name (str)`: Nombre de la categoría, único y con un máximo de 50 caracteres.
        `user_id (ForeignKey)`: Relación con el modelo User, indica el creador de la categoría.
        `parent_category_id (ForeignKey)`: Categoría padre a la que pertenece esta categoría (autorreferencia).
        `recipes (ManyToManyField)`: Lista de recetas asociadas a esta categoría.
        `ingredients (ManyToManyField)`: Lista de ingredientes asociados a esta categoría.
        'created_at': Registro de la hora de creación.

    Notas:
        Todos los campos son de solo lectura para este serializer, ya que se utiliza principalmente para visualización.

    Author:
        Ana Castro
    """
    recipes = RecipeSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    parent_category = models.ForeignKey('self', related_name='child_categories', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:

        model = Category
        fields = ['id', 'name', 'user_id', 'parent_category_id', 'recipes', 'ingredients']
        read_only_fields = ['id', 'name', 'user_id', 'parent_category_id', 'recipes', 'ingredients']

class CategoryAdminSerializer(serializers.ModelSerializer):
    """
    Serializer de Category para administrador, representa las diferentes categorías asociadas a recetas e ingredientes.

    Args:
        serializers.ModelSerializer: Clase base de DRF para serializers basados en modelos.

    Attributes:
        `id (int)`: Identificador único de la categoría.
        'created_at': Registro de la hora de creación

    Notas:
        Solo el admin puede acturalizar todos los campos menos el id y la hora de creación que lo realiza django internamente.

    Author:
        Ana Castro
    """
    recipes = RecipeSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
