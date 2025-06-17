from rest_framework import serializers
from recipes.models.recipe import Recipe
from recipes.models.category import Category
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.step import Step
from recipes.serializers.stepSerializer import StepSerializer
from users.serializers.userSerializer import CustomUserSerializer, CustomUserFrontSerializer
from .recipeIngredientSerializer import RecipeIngredientSerializer
from media.models.image import Image
from media.serializers.image_serializer import ImageListSerializer


class RecipeSerializer(serializers.ModelSerializer):

    """
    Serializer para el modelo Recipe utilizado en vistas públicas o de uso general.

    Args:
        serializers (ModelSerializer): Clase base de DRF que serializa instancias del modelo a datos JSON y viceversa.

    Attributes:
        `user (CustomUserFrontSerializer)`: Campo de solo lectura que representa el usuario creador de la receta (anidado). 
        `categories (PrimaryKeyRelatedField)`: Lista de categorías asociadas a la receta, permite múltiples relaciones (ManyToMany).

    Meta:
        model (Recipe): Modelo de la base de datos a serializar.  
        fields (list): Lista de campos incluidos en la representación JSON.  
        read_only_fields (list): Lista de campos que no pueden modificarse a través del serializer.

    Campos expuestos:
        `id (int)`: Identificador único de la receta.  
        `name (str)`: Nombre de la receta.  
        `description (str)`: Descripción breve de la receta.  
        `user (obj)`: Objeto del usuario que creó la receta (con id y username).
        `duration_minutes (int)`: Tiempo estimado de preparación.  
        `commensals (int)`: Número de comensales para los que rinde la receta.  
        `categories (list[int])`: IDs de las categorías a las que pertenece la receta.  
        `steps (list[obj])`: Lista de pasos de la receta.
        `ingredients (list[obj])`: Lista de ingredientes de la receta.
        `updated_at (datetime)`: Fecha de la última modificación del registro (solo lectura).
        `image (str)`: URL de la imagen principal de la receta.

    Author:
        Lorena Martínez
    """

    user = CustomUserFrontSerializer(read_only=True, source='user_id')
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    ingredients = RecipeIngredientSerializer(many=True, read_only=True, source='recipe_ingredients')
    steps = StepSerializer(many=True, read_only=True, source='step_set')
    image = serializers.SerializerMethodField()

    class Meta:

        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'ingredients',
            'user',
            'duration_minutes',
            'commensals',
            'categories', 
            'steps',
            'updated_at',
            'image'
        ]

        read_only_fields = ['id', 'user', 'updated_at']

    def get_image(self, obj):
        image = Image.objects.filter(external_id=obj.id, type='RECIPE').first()
        return ImageListSerializer(image).data if image else None


class RecipeAdminSerializer(serializers.ModelSerializer):

    """
    Serializer para el modelo Recipe con acceso completo a todos los campos.
    Diseñado para usuarios con permisos administrativos o necesidades internas.

    Args:
        serializers (ModelSerializer): Clase base de DRF que serializa instancias del modelo a datos JSON y viceversa.

    Attributes:
        `user_id (PrimaryKeyRelatedField)`: Campo que representa el ID del usuario creador (para escritura y lectura por admin).
        `categories (PrimaryKeyRelatedField)`: Lista de IDs de categorías asociadas.

    Meta:
        model (Recipe): Modelo de base de datos a serializar.  
        fields (str): Inclusión de todos los campos del modelo.  
        read_only_fields (list): Campos que no deben modificarse directamente.

    Campos expuestos (todos los campos del modelo):
        Incluye `created_at` y `updated_at`, además de los campos de receta estándar.

    Author:
        {Lorena Martínez}
    Modified:
        {Ana Castro}
    """
    
    user = CustomUserFrontSerializer(read_only=True, source='user_id')
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    steps = StepSerializer(many=True, read_only=True, source='step_set')
    ingredients = RecipeIngredientSerializer(many=True, read_only=True, source='recipe_ingredients')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_id']

    def get_image(self, obj):
        image = Image.objects.filter(external_id=obj.id, type='RECIPE').first()
        return ImageListSerializer(image).data['url'] if image else None