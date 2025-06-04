from rest_framework import serializers
from recipes.models.recipe import Recipe
from recipes.models.category import Category


class RecipeSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

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
            'updated_at'
        ]

        read_only_fields = ['id','user_id', 'updated_at']


class RecipeAdminSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id','user_id', 'created_at', 'updated_at']
