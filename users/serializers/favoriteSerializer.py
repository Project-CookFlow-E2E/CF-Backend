from rest_framework import serializers
from users.models.favorite import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer de Favorite, representa las diferentes categorías asociadas a recetas e ingredientes.

    Args:
        serializers.ModelSerializer: Clase base de DRF para serializers basados en modelos.

    Attributes:
        `id (int)`: Identificador único de la categoría.
        'user_id'(ForeignKey)`: Relación con el modelo User, indica el creador de la categoría.
        'recipe_id'(ForeignKey)`: Receta asociada.

    Notas:
        Se pueden actualizar el usuario asociado a la receta favorita y la receta en si, pero la id no porque la crea\n
        django internamente.

    Author:
        Ana Castro
    """

    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'recipe_id']
        read_only_fields = ['id']


class FavoriteAdminSerializer(serializers.ModelSerializer):
    """
    Serializer de Favorite de admin, representa las diferentes categorías asociadas a recetas e ingredientes.

    Args:
        serializers.ModelSerializer: Clase base de DRF para serializers basados en modelos.

    Attributes:
        `id (int)`: Identificador único de la categoría.
        'user_id'(ForeignKey)`: Relación con el modelo User, indica el creador de la categoría.
        'recipe_id'(ForeignKey)`: Receta asociada.
        'created_at': Registro de la hora de creación.

    Notas:
        Se pueden actualizar el usuario asociado a la receta favorita y la receta en si, pero la id y la hora de creacion no\n
        porque la crea django internamente.

    Author:
        Ana Castro
    """

    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'recipe_id', 'created_at']
        read_only_fields = ['id', 'created_at']
