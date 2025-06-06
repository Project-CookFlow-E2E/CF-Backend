from rest_framework.routers import DefaultRouter
from recipes.views.ingredientViewSet import IngredientViewSet, IngredientAdminViewSet
from recipes.views.step_viewset import StepViewSet, StepAdminViewSet
router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)  # Registra el ViewSet de ingredientes
router.register(r'admin/ingredients', IngredientAdminViewSet)
router.register(r'steps', StepViewSet)
router.register(r'admin/steps', StepAdminViewSet)
urlpatterns = router.urls

