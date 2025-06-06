from rest_framework import viewsets
from shopping.models.shoppingListItem import ShoppingListItem
from shopping.serializers.shoppingListItemSerializer import ShoppingListItemSerializer

class ShoppingListItemView(viewsets.ModelViewSet):
    """ViewSet para gestionar directamente la lista de la compra del usuario, compuesta\n
    por ítems individuales. Hace un CRUD completo
    Author:
        {Ana Castro}"""
    queryset = ShoppingListItem.objects.all()
    serializer_class = ShoppingListItemSerializer
