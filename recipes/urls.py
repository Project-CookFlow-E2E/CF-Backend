from rest_framework.routers import DefaultRouter
from recipes.views.ingredientViewset import IngredientViewSet, IngredientAdminViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)  # Registra el ViewSet de ingredientes
router.register(r'admin/ingrdients', IngredientAdminViewSet)
urlpatterns = router.urls