from rest_framework.routers import DefaultRouter
from django.urls import path, include
from shopping.views.shoppingListItemView import ShoppingListItemView

router = DefaultRouter()
router.register(r'items', ShoppingListItemView)

urlpatterns = [
    path('', include(router.urls)),
]
