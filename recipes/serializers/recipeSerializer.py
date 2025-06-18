# recipes/serializers/recipeSerializer.py

from rest_framework import serializers
from recipes.models.recipe import Recipe
from recipes.models.category import Category
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.step import Step
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit # Usamos Unit, confirma que este es tu modelo de unidades

from recipes.serializers.stepSerializer import StepSerializer
from users.serializers.userSerializer import CustomUserFrontSerializer
from .recipeIngredientSerializer import RecipeIngredientSerializer
from media.models.image import Image
from media.serializers.image_serializer import ImageListSerializer

# Importa el servicio de imágenes
from media.services.image_service import update_image_for_instance

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
        request = self.context.get('request')
        print("\n--- DEBUG: Entering RecipeSerializer.create() ---")
        print(f"DEBUG: validated_data keys: {validated_data.keys()}")
        print(f"DEBUG: request.FILES keys: {request.FILES.keys()}")

        print(f"DEBUG: Tipo de request.data: {type(request.data)}")
        print(f"DEBUG: Contenido de request.data: {request.data}")

        ingredients_json = request.data.get('ingredients_data', '[]')
        steps_json = request.data.get('steps_data', '[]')

        # === FIX PARA CATEGORIAS ===
        # Ahora las categorías vienen como una lista bajo la clave 'categories' en request.data
        categories_ids = request.data.get('categories', []) # <--- LÍNEA CORREGIDA
        print(f"DEBUG: IDs de categorías desde request.data.get('categories'): {categories_ids}")


        try:
            parsed_ingredients = json.loads(ingredients_json)
        except json.JSONDecodeError:
            raise serializers.ValidationError({"ingredients_data": "Formato JSON de ingredientes inválido."})

        try:
            parsed_steps = json.loads(steps_json)
        except json.JSONDecodeError:
            raise serializers.ValidationError({"steps_data": "Formato JSON de pasos inválido."})

        # === FIX PARA KeyError: 'user' ===
        # 'validated_data' contiene 'user_id', no 'user'.
        user = validated_data.pop('user_id') # <--- LÍNEA CORREGIDA


        # Asegúrate de eliminar 'categories' de validated_data si lo tienes, ya que lo gestionamos aparte.
        validated_data.pop('categories', None)

        recipe = Recipe.objects.create(user_id=user, **validated_data)
        print(f"DEBUG: Receta creada con ID: {recipe.id}")

        if categories_ids:
            recipe.categories.set(categories_ids)
            print(f"DEBUG: Categorías asignadas a la receta {recipe.id}: {categories_ids}")

        for ing_data in parsed_ingredients:
            ingredient_id = ing_data.get('ingredient')
            quantity = ing_data.get('quantity')
            unit_id = ing_data.get('unit')

            if not all([ingredient_id, quantity, unit_id]):
                raise serializers.ValidationError("Datos incompletos para el ingrediente de la receta.")

            try:
                ingredient = Ingredient.objects.get(id=ingredient_id)
                unit_obj = Unit.objects.get(id=unit_id)
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity,
                    unit=unit_obj
                )
                print(f"DEBUG: Ingrediente de receta creado para receta {recipe.id}, ingrediente {ingredient_id}")
            except (Ingredient.DoesNotExist, Unit.DoesNotExist) as e:
                print(f"ERROR: Ingrediente o unidad no encontrado durante la creación: {e}")
                raise serializers.ValidationError(f"Ingrediente o unidad no encontrado: {e}")

        # === La parte de los archivos sigue esperando que vengan en request.FILES ===
        recipe_photo_file = request.FILES.get('photo')
        print(f"DEBUG: archivo de foto de receta recibido: {recipe_photo_file.name if recipe_photo_file else 'None'}")
        if recipe_photo_file:
            print("DEBUG: Llamando a update_image_for_instance para la foto de la receta...")
            update_image_for_instance(
                image_file=recipe_photo_file,
                user_id=request.user.id,
                external_id=recipe.id,
                image_type=Image.ImageType.RECIPE
            )
            print("DEBUG: update_image_for_instance para la foto de la receta finalizado.")
        else:
            print("DEBUG: No se proporcionó archivo de foto de receta en request.FILES.")


        for idx, step_data in enumerate(parsed_steps):
            order = step_data.get('order')
            text = step_data.get('description')

            if not all([order, text]):
                raise serializers.ValidationError(f"Datos incompletos para el paso {idx+1}.")

            step_obj = Step.objects.create(
                recipe=recipe,
                order=order,
                description=text,
            )
            print(f"DEBUG: Paso {idx} creado con ID: {step_obj.id}")

            step_image_file = request.FILES.get(f'step_image_{idx}')
            print(f"DEBUG: archivo de imagen de paso {idx} recibido: {step_image_file.name if step_image_file else 'None'}")
            if step_image_file:
                print(f"DEBUG: Llamando a update_image_for_instance para step_image_{idx}...")
                update_image_for_instance(
                    image_file=step_image_file,
                    user_id=request.user.id,
                    external_id=step_obj.id,
                    image_type=Image.ImageType.STEP
                )
                print(f"DEBUG: update_image_for_instance para step_image_{idx} finalizado.")
            else:
                print(f"DEBUG: No se proporcionó archivo de imagen para el paso {idx} en request.FILES.")

        print("--- DEBUG: Saliendo de RecipeSerializer.create() ---")
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

    # Si el RecipeAdminSerializer también va a manejar subidas de imágenes
    # y los mismos campos que el RecipeSerializer regular, deberías copiar
    # el método 'create' corregido de arriba también aquí.
    # Por ahora, dejo tu 'create' original para RecipeAdminSerializer.
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