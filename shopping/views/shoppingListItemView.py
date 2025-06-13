from rest_framework import viewsets
from shopping.models.shoppingListItem import ShoppingListItem
from shopping.serializers.shoppingListItemSerializer import ShoppingListItemSerializer, ShoppingListItemAdminSerializer
from rest_framework.permissions import IsAuthenticated

class ShoppingListItemView(viewsets.ModelViewSet):
    """ViewSet para gestionar directamente la lista de la compra del usuario, compuesta\n
    por ítems individuales. Hace un CRUD completo en su lista, el admin puede hacerlo en todas
    Author:
        {Ana Castro}"""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ShoppingListItem.objects.all()
        return ShoppingListItem.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ShoppingListItemAdminSerializer
        return ShoppingListItemSerializer
