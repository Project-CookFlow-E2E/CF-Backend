from rest_framework import serializers
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.recipe import Recipe
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit

class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo RecipeIngredient.

    Convierte los objetos RecipeIngredient en formato JSON y gestiona la relación con Recipe e Ingredient. 
    Este serializer permite la creación y consulta de los ingredientes asociados a una receta, asegurando 
    que los campos claves sean tratados adecuadamente.

    Attributes:
        id (int, read-only): Identificador único del RecipeIngredient, solo lectura.
        recipe (int): ID de la receta asociada (relación con Recipe).
        ingredient (int): ID del ingrediente asociado (relación con Ingredient).
        quantity (int): Cantidad del ingrediente dentro de la receta.
        unit (str): Unidad de medida para la cantidad del ingrediente.
        created_at (datetime, read-only): Fecha y hora en que se creó el registro, solo lectura.

    Meta:
        model (RecipeIngredient): Modelo RecipeIngredient.
        fields (tuple): Campos incluidos en la representación JSON.
        read_only_fields (tuple): Campos que no pueden ser modificados desde la API.
    
    Author:
        {Rafael Fernández}
    Modified:
        {Ana Castro}
    """
    
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all()) 
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())  

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'ingredient', 'quantity', 'unit']
        read_only_fields = ['id']


class RecipeIngredientAdminSerializer(serializers.ModelSerializer):
    """
    Serializer para RecipeIngredient.

    Este serializer proporciona acceso completo a todos los atributos del modelo RecipeIngredient, 
    pero restringe la modificación de ciertos campos claves como `created_at`, `id`, `recipe` y `ingredient`.

    Attributes:
        id (int, read-only): Identificador único de RecipeIngredient, solo lectura.
        recipe (int, read-only): ID de la receta asociada (relación con Recipe).
        ingredient (int, read-only): ID del ingrediente asociado (relación con Ingredient).
        quantity (int): Cantidad del ingrediente en la receta.
        unit (str): Unidad de medida de la cantidad del ingrediente.
        created_at (datetime, read-only): Fecha y hora de creación del registro, solo lectura.

    Meta:
        model (RecipeIngredient): Modelo RecipeIngredient.
        fields (str): Incluye todos los campos del modelo.
        read_only_fields (tuple): Lista de campos que no pueden ser modificados desde la API.

    Author:
        {Rafael Fernández}
    """
    
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())  
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all()) 
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())  

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
        read_only_fields = ['id', 'created_at']