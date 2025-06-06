from rest_framework.routers import DefaultRouter
from recipes.views.ingredientViewSet import IngredientViewSet, IngredientAdminViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)  # Registra el ViewSet de ingredientes
router.register(r'admin/ingredients', IngredientAdminViewSet)
urlpatterns = [
    path('', include(router.urls)),
]