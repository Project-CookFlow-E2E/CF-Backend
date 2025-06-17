from rest_framework import serializers
from recipes.serializers.ingredientFromSerializer import IngredientFromSerializer
from recipes.serializers.ingredientSerializer import IngredientSerializer
from shopping.models.shoppingListItem import ShoppingListItem
from users.models.user import CustomUser
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit

class ShoppingListItemSerializer(serializers.ModelSerializer):

    """
    Serializer para el modelo ShoppingListItem, utilizado en vistas de usuarios estándar.

    Args:
        serializers (ModelSerializer): Clase base de DRF para serialización de modelos.

    Attributes:
        `user_id (PrimaryKeyRelatedField)`: Campo de solo lectura que representa el ID del usuario que posee el ítem.  
        `ingredient_id (PrimaryKeyRelatedField)`: Campo de solo lectura que representa el ID del ingrediente asociado.

    Meta:
        model (ShoppingListItem): Modelo que representa un ítem de la lista de la compra.  
        fields (list): Lista de campos incluidos en la serialización.  
        read_only_fields (list): Campos que no pueden ser modificados desde el serializer.

    Campos expuestos:
        `user_id (int)`: ID del usuario propietario del ítem.  
        `ingredient_id (int)`: ID del ingrediente asociado.  
        `quantity_needed (int)`: Cantidad requerida del ingrediente.  
        `unit (str)`: Unidad de medida correspondiente (ej. gramos, litros, etc.).  
        `is_purchased (bool)`: Estado de compra del ingrediente.

    Author:
        Lorena Martínez
    """

    # ingredient_id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), allow_null=True, required=False)
    ingredient = IngredientFromSerializer(read_only=True, source='ingredient_id')

    class Meta:
        model = ShoppingListItem
        fields = [
            'id',                  # 👈 este es el que necesitas para el DELETE
            'user_id',
            'ingredient',          # muestra el objeto (name, id)
            'ingredient_id',       # 👈 también añade esto si lo necesitas en frontend
            'quantity_needed',
            'unit',
            'is_purchased',
        ]

        read_only_fields = ['user_id']


class ShoppingListItemAdminSerializer(serializers.ModelSerializer):

    """
    Serializer para el modelo ShoppingListItem con acceso completo para administradores.

    Args:
        serializers (ModelSerializer): Clase base de DRF para serialización de modelos.

    Attributes:
        `user_id (PrimaryKeyRelatedField)`: Campo de solo lectura que representa el ID del usuario propietario.  
        `ingredient_id (PrimaryKeyRelatedField)`: Campo de solo lectura que representa el ID del ingrediente.

    Meta:
        model (ShoppingListItem): Modelo de ítem de lista de compras.  
        fields (str): Inclusión de todos los campos del modelo.  
        read_only_fields (list): Campos no editables desde el serializer, incluso para administradores.

    Campos expuestos:
        Todos los campos del modelo, incluyendo:
        - `created_at (datetime)`: Fecha de creación del registro.  
        - `updated_at (datetime)`: Última fecha de actualización.  
        - `quantity_needed`, `unit`, `is_purchased`, entre otros.

    Author:
        Lorena Martínez
    """

    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    ingredient_id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), allow_null=True, required=False)

    class Meta:
        model = ShoppingListItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
