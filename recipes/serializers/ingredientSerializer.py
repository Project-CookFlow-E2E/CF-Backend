from rest_framework import serializers
from models.ingredient import Ingredient
from models.recipe import RecipeIngredient
from models.shopping_list import ShoppingListItem

class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer de Ingredient, representa los ingredientes que pueden aparecer tanto en recetas
    como en listas de la compra, y ser gestionados por usuarios o administradores.

    Lógica aplicada:
    - Campos básicos accesibles a cualquier usuario.
    - Si el contexto incluye información de recetas, se mostrarán `quantity` y `unit`.
    - Si el contexto incluye la lista de la compra, se mostrará `is_checked`.
    - Si el usuario es administrador, se mostrarán más campos como `created_at`, `updated_at`, etc.

    Este serializer unifica la lógica para simplificar el mantenimiento y asegurar consistencia.

    Author:
        Noemi Casaprima 
    """


    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'description',
            'quantity',
            'unit',
            'is_checked',
           
        ]
        read_only_fields = ['id']


class IngredientAdminSerializer(serializers.ModelSerializer):
    """
    Serializer exclusivo para usuarios administradores. Permite el acceso completo
    al modelo Ingredient para lectura y escritura, excepto a campos generados automáticamente
    como el ID o timestamps.

    Esta clase está diseñada para tareas de mantenimiento, carga masiva, y ajustes internos
    que solo debe realizar un perfil con permisos de administrador.

    Author:
        Noemi Casaprima 
    """

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at'] 








    # def get_quantity(self, obj):
    #     """
    #     Devuelve la cantidad asociada si el ingrediente forma parte de una receta.
    #     """
    #     recipe_ingredients = self.context.get('recipe_ingredients', {}) 
    #     # donde la clave es el id del ingrediente y el valor es el objeto RecipeIngredient
    #     # que contiene la cantidad y unidad.
    #     recipe_ingredient = recipe_ingredients.get(obj.id) 
    #     # Si el ingrediente no está en la receta, devuelve None
    #     return recipe_ingredient.quantity if recipe_ingredient else None

    # def get_unit(self, obj): 
    #     """
    #     Devuelve la unidad de medida si el ingrediente forma parte de una receta.
    #     """
    #     recipe_ingredients = self.context.get('recipe_ingredients', {}) 
    #     # donde la clave es el id del ingrediente y el valor es el objeto RecipeIngredient
    #     # que contiene la cantidad y unidad.
    #     # Obtiene el RecipeIngredient correspondiente al ingrediente
    #     recipe_ingredient = recipe_ingredients.get(obj.id)
    #     # Si el ingrediente no está en la receta, devuelve None
    #     return recipe_ingredient.unit if recipe_ingredient else None

    # def get_is_checked(self, obj):
    #     """
    #     Devuelve el estado del ingrediente en la lista de la compra si aplica.
    #     """
    #     shopping_list = self.context.get('shopping_list', {}) 
    #     # donde la clave es el id del ingrediente y el valor es el objeto ShoppingListItem  
    #     # que contiene el estado de verificación.
    #     # Obtiene el ShoppingListItem correspondiente al ingrediente    
    #     item = shopping_list.get(obj.id)
    #     return item.is_checked if item else None #Si el ingrediente no está en la lista de la compra, devuelve None
    

    # def to_representation(self, instance):
    #     """
    #     Personaliza la salida según el tipo de usuario.
    #     """
    #     rep = super().to_representation(instance) # Llama al método padre para obtener la representación básica
        
    #     user = self.context['request'].user # Obtiene el usuario de la solicitud

    #     if not user.is_staff:
    #         rep.pop('created_at', None) # Elimina el campo 'created_at' para usuarios normales
    #         rep.pop('updated_at', None) # Elimina el campo 'updated_at' para usuarios normales
    #     return rep
