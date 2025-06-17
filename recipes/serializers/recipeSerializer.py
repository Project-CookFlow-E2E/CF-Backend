from rest_framework import serializers
from recipes.models.recipe import Recipe
from recipes.models.category import Category
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.step import Step
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit

from recipes.serializers.stepSerializer import StepSerializer
from users.serializers.userSerializer import CustomUserFrontSerializer
from .recipeIngredientSerializer import RecipeIngredientSerializer
from media.models.image import Image
from media.serializers.image_serializer import ImageListSerializer

import json


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

        Modified by:
            Saturnino Mendez
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

    def create(self, validated_data):
        steps_data_str = self.context['request'].data.get('steps')
        ingredients_data_str = self.context['request'].data.get('ingredients')

        # Extraer las categorías de validated_data
        # Si categories no está en validated_data, se usará una lista vacía
        categories_data = validated_data.pop('categories', []) # <--- ¡CAMBIO AQUÍ!

        ingredients_data = []
        steps_data = []

        if ingredients_data_str:
            try:
                ingredients_data = json.loads(ingredients_data_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"ingredients": "Formato JSON de ingredientes inválido."})

        if steps_data_str:
            try:
                steps_data = json.loads(steps_data_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"steps": "Formato JSON de pasos inválido."})

        # Crear la receta S-I-N categorías
        recipe = Recipe.objects.create(**validated_data) # <--- AHORA validated_data NO contiene 'categories'

        # Asignar las categorías después de crear la receta
        if categories_data: # Solo si hay categorías para asignar
            recipe.categories.set(categories_data) # <--- ¡CAMBIO AQUÍ!

        for item in ingredients_data:
            try:
                ingredient_obj = Ingredient.objects.get(id=item['ingredient'])
                unit_obj = Unit.objects.get(id=item['unit'])
            except (Ingredient.DoesNotExist, Unit.DoesNotExist) as e:
                raise serializers.ValidationError(
                    {"detail": f"Ingrediente o unidad no encontrado: {e}. Asegúrate de que los IDs existan."}
                ) from e

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_obj,
                quantity=item['quantity'],
                unit=unit_obj,
            )

        for item in steps_data:
            Step.objects.create(
                recipe=recipe,
                order=item['order'],
                description=item['description'],
            )

        return recipe

    def update(self, instance, validated_data):

        """
        Actualiza una instancia existente de Recipe y sus ingredientes/pasos asociados.

        Actualiza los campos directos de la receta, y gestiona las relaciones Many-to-Many
        (categorías) y anidadas (ingredientes, pasos) comparando los datos existentes
        con los recibidos.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.duration_minutes = validated_data.get('duration_minutes', instance.duration_minutes)
        instance.commensals = validated_data.get('commensals', instance.commensals)

        categories_data = validated_data.get('categories')
        if categories_data is not None:
            instance.categories.set(categories_data)

        instance.save()

        ingredients_data_str = self.context['request'].data.get('ingredients')
        if ingredients_data_str is not None:
            try:
                new_ingredients_data = json.loads(ingredients_data_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"ingredients": "Formato JSON de ingredientes inválido para actualización."})

            current_ingredients = {ri.ingredient_id: ri for ri in instance.recipe_ingredients.all()}
            new_ingredient_ids_set = {item['ingredient'] for item in new_ingredients_data}

            for item in new_ingredients_data:
                ing_id = item['ingredient']
                qty = item['quantity']
                unit_id = item['unit']

                try:
                    ingredient_obj = Ingredient.objects.get(id=ing_id)
                    unit_obj = Unit.objects.get(id=unit_id)
                except (Ingredient.DoesNotExist, Unit.DoesNotExist) as e:
                    raise serializers.ValidationError(
                        {"detail": f"Ingrediente o unidad no encontrado para actualizar: {e}. ID: {ing_id}"}
                    ) from e

                if ing_id in current_ingredients:
                    ri_instance = current_ingredients[ing_id]
                    ri_instance.quantity = qty
                    ri_instance.unit = unit_obj
                    ri_instance.save()
                else:
                    RecipeIngredient.objects.create(
                        recipe=instance,
                        ingredient=ingredient_obj,
                        quantity=qty,
                        unit=unit_obj
                    )

            for ing_id_to_delete, ri_instance in current_ingredients.items():
                if ing_id_to_delete not in new_ingredient_ids_set:
                    ri_instance.delete()

        steps_data_str = self.context['request'].data.get('steps')
        if steps_data_str is not None:
            try:
                new_steps_data = json.loads(steps_data_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"steps": "Formato JSON de pasos inválido para actualización."})

            current_steps = {s.order: s for s in instance.step_set.all()}
            new_step_orders_set = {item['order'] for item in new_steps_data}

            for item in new_steps_data:
                order = item['order']
                description = item['description']

                if order in current_steps:
                    step_instance = current_steps[order]
                    step_instance.description = description
                    step_instance.save()
                else:
                    Step.objects.create(
                        recipe=instance,
                        order=order,
                        description=description
                    )

            for order_to_delete, step_instance in current_steps.items():
                if order_to_delete not in new_step_orders_set:
                    step_instance.delete()

        return instance


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
        {Ana Castro, Saturnino Mendez}
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

    def create(self, validated_data):

        """
            Crea una nueva instancia de Recipe y sus ingredientes/pasos asociados,
            con un enfoque para el uso administrativo.

            Extrae las categorías, ingredientes y pasos del `validated_data` y de `request.data`.
            Crea la instancia de la receta, y luego itera para crear los RecipeIngredient y Step.
        """
        ingredients_data_str = self.context['request'].data.get('ingredients')
        steps_data_str = self.context['request'].data.get('steps')

        # Extraer las categorías de validated_data
        categories_data = validated_data.pop('categories', []) # <--- ¡CAMBIO AQUÍ!

        ingredients_data = []
        steps_data = []

        if ingredients_data_str:
            try:
                ingredients_data = json.loads(ingredients_data_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"ingredients": "Formato JSON de ingredientes inválido."})

        if steps_data_str:
            try:
                steps_data = json.loads(steps_data_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"steps": "Formato JSON de pasos inválido."})

        # Crear la receta S-I-N categorías
        recipe = Recipe.objects.create(**validated_data)

        # Asignar las categorías después de crear la receta
        if categories_data: # Solo si hay categorías para asignar
            recipe.categories.set(categories_data)

        for item in ingredients_data:
            try:
                ingredient_obj = Ingredient.objects.get(id=item['ingredient'])
                unit_obj = Unit.objects.get(id=item['unit'])
            except (Ingredient.DoesNotExist, Unit.DoesNotExist) as e:
                raise serializers.ValidationError(
                    {"detail": f"Ingrediente o unidad no encontrado: {e}. Asegúrate de que los IDs existan."}
                ) from e

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_obj,
                quantity=item['quantity'],
                unit=unit_obj,
            )

        for item in steps_data:
            Step.objects.create(
                recipe=recipe,
                order=item['order'],
                description=item['description'],
            )

        return recipe

    def update(self, instance, validated_data):
        """
            Actualiza una instancia existente de Recipe y sus ingredientes/pasos asociados,
            con un enfoque para el uso administrativo.

            Actualiza los campos directos de la receta, y gestiona las relaciones Many-to-Many
            (categorías) y anidadas (ingredientes, pasos) comparando los datos existentes
            con los recibidos.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.duration_minutes = validated_data.get('duration_minutes', instance.duration_minutes)
        instance.commensals = validated_data.get('commensals', instance.commensals)

        categories_data = validated_data.get('categories')
        if categories_data is not None:
            instance.categories.set(categories_data)

        instance.save()

        ingredients_data_str = self.context['request'].data.get('ingredients')
        if ingredients_data_str is not None:
            try:
                new_ingredients_data = json.loads(ingredients_data_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"ingredients": "Formato JSON de ingredientes inválido para actualización."})

            current_ingredients = {ri.ingredient_id: ri for ri in instance.recipe_ingredients.all()}
            new_ingredient_ids_set = {item['ingredient'] for item in new_ingredients_data}

            for item in new_ingredients_data:
                ing_id = item['ingredient']
                qty = item['quantity']
                unit_id = item['unit']

                try:
                    ingredient_obj = Ingredient.objects.get(id=ing_id)
                    unit_obj = Unit.objects.get(id=unit_id)
                except (Ingredient.DoesNotExist, Unit.DoesNotExist) as e:
                    raise serializers.ValidationError(
                        {"detail": f"Ingrediente o unidad no encontrado para actualizar: {e}. ID: {ing_id}"}
                    ) from e

                if ing_id in current_ingredients:
                    ri_instance = current_ingredients[ing_id]
                    ri_instance.quantity = qty
                    ri_instance.unit = unit_obj
                    ri_instance.save()
                else:
                    RecipeIngredient.objects.create(
                        recipe=instance,
                        ingredient=ingredient_obj,
                        quantity=qty,
                        unit=unit_obj
                    )

            for ing_id_to_delete, ri_instance in current_ingredients.items():
                if ing_id_to_delete not in new_ingredient_ids_set:
                    ri_instance.delete()

        steps_data_str = self.context['request'].data.get('steps')
        if steps_data_str is not None:
            try:
                new_steps_data = json.loads(steps_data_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"steps": "Formato JSON de pasos inválido para actualización."})

            current_steps = {s.order: s for s in instance.step_set.all()}
            new_step_orders_set = {item['order'] for item in new_steps_data}

            for item in new_steps_data:
                order = item['order']
                description = item['description']

                if order in current_steps:
                    step_instance = current_steps[order]
                    step_instance.description = description
                    step_instance.save()
                else:
                    Step.objects.create(
                        recipe=instance,
                        order=order,
                        description=description
                    )

            for order_to_delete, step_instance in current_steps.items():
                if order_to_delete not in new_step_orders_set:
                    step_instance.delete()

        return instance