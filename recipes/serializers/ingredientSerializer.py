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
    