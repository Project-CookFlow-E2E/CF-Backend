from rest_framework.routers import DefaultRouter
from recipes.views.ingredientViewSet import IngredientViewSet, IngredientAdminViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)  # Registra el ViewSet de ingredientes
router.register(r'admin/ingredients', IngredientAdminViewSet)
urlpatterns = router.urls