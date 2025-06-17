from rest_framework import serializers
from recipes.models.ingredient import Ingredient


class IngredientFromSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
        ]

        read_only_fields = ['id', 'created_at', 'updated_at']


class IngredientAdminFromSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
