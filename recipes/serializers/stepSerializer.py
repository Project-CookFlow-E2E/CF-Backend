from rest_framework import serializers
from recipes.models import Step

class StepSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Step.

    Este serializer convierte los objetos de la tabla `Step` en datos JSON
    y permite la creación y actualización de los campos `order` y `description`.

    Attributes:
        order (int): Número de orden del paso dentro de la receta.
        description (str): Descripción del paso de la receta.
        id (int, read-only): Identificador único del paso, solo lectura.
        recipe_id (int, read-only): Identificador de la receta asociada, solo lectura.

    Meta:
        model (Step): Modelo Step.
        fields (tuple): Campos a incluir en la representación JSON.
        read_only_fields (tuple): Campos que no pueden ser modificados por la API.
     Author:  
        {Rafael Fernández}
    """

    class Meta:
        model = Step
        fields = ( 'id','order', 'description','recipe_id')  
        read_only_fields = ('id', 'recipe_id')

class StepAdminSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Step.

    Permite acceder a todos los campos del modelo `Step`,
    pero restringe la modificación de `created_at`, `updated_at`, `id` y `recipe_id`.

    Attributes:
        id (int, read-only): Identificador único del paso, solo lectura.
        order (int): Número de orden del paso dentro de la receta.
        description (str): Descripción del paso de la receta.
        recipe_id (int, read-only): Identificador de la receta asociada, solo lectura.
        created_at (datetime, read-only): Fecha y hora de creación, solo lectura.
        updated_at (datetime, read-only): Fecha y hora de última actualización, solo lectura.

    Meta:
        model (Step): Modelo Step.
        fields (str): Incluir todos los campos del modelo.
        read_only_fields (tuple): Lista de campos que no pueden ser modificados.
    Author:  
        {Rafael Fernández}
    """

    class Meta:
        model = Step
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'id', 'recipe_id')

