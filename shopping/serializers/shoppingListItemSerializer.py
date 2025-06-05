from rest_framework import serializers
from shopping.models.shoppingListItem import ShoppingListItem


class ShoppingListItemSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ShoppingListItem
        fields = [
            'user_id',
            'ingredient_id',
            'quantity_needed',
            'unit',
            'is_purchased'
        ]

        read_only_fields = ['user_id', 'ingredient_id']


class ShoppingListItemAdminSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ShoppingListItem
        fields = '__all__'
        read_only_fields = ['id','user_id', 'ingredient_id', 'created_at', 'updated_at']
