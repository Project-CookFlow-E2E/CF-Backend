from rest_framework import serializers
from recipes.models.recipe import Recipe
from recipes.models.category import Category
from recipes.models.step import Step
from recipes.serializers.stepSerializer import StepSerializer

class RecipeSerializer(serializers.ModelSerializer):

    """
    Serializer para el modelo Recipe utilizado en vistas públicas o de uso general.

    Args:
        serializers (ModelSerializer): Clase base de DRF que serializa instancias del modelo a datos JSON y viceversa.

    Attributes:
        `user_id (PrimaryKeyRelatedField)`: Campo de solo lectura que representa el ID del usuario creador de la receta.  
        `categories (PrimaryKeyRelatedField)`: Lista de categorías asociadas a la receta, permite múltiples relaciones (ManyToMany).

    Meta:
        model (Recipe): Modelo de la base de datos a serializar.  
        fields (list): Lista de campos incluidos en la representación JSON.  
        read_only_fields (list): Lista de campos que no pueden modificarse a través del serializer.

    Campos expuestos:
        `id (int)`: Identificador único de la receta.  
        `name (str)`: Nombre de la receta.  
        `description (str)`: Descripción breve de la receta.  
        `user_id (int)`: ID del usuario que creó la receta.  
        `duration_minutes (int)`: Tiempo estimado de preparación.  
        `commensals (int)`: Número de comensales para los que rinde la receta.  
        `categories (list[int])`: IDs de las categorías a las que pertenece la receta.  
        `updated_at (datetime)`: Fecha de la última modificación del registro (solo lectura).

    Author:
        Lorena Martínez
"""

    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    steps = StepSerializer(many=True, read_only=True, source='step_set')
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'user_id',
            'duration_minutes',
            'commensals',
            'categories', 
            'steps',
            'updated_at'
        ]

        read_only_fields = ['id','user_id', 'updated_at']


class RecipeAdminSerializer(serializers.ModelSerializer):

    """
    Serializer para el modelo Recipe con acceso completo a todos los campos.
    Diseñado para usuarios con permisos administrativos o necesidades internas.

    Args:
        serializers (ModelSerializer): Clase base de DRF que serializa instancias del modelo a datos JSON y viceversa.

    Attributes:
        `user_id (PrimaryKeyRelatedField)`: Campo de solo lectura que representa el ID del usuario creador.  
        `categories (PrimaryKeyRelatedField)`: Lista de IDs de categorías asociadas.

    Meta:
        model (Recipe): Modelo de base de datos a serializar.  
        fields (str): Inclusión de todos los campos del modelo.  
        read_only_fields (list): Campos que no deben modificarse directamente.

    Campos expuestos (todos los campos del modelo):
        Incluye `created_at` y `updated_at`, además de los campos de receta estándar.

    Author:
        Lorena Martínez
    """
    
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    steps = StepSerializer(many=True, read_only=True, source='step_set')

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id','user_id', 'created_at', 'updated_at']
