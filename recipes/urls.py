from rest_framework.routers import DefaultRouter
from recipes.views.recipeView import RecipeViewSet
from recipes.views.ingredientViewSet import IngredientViewSet, IngredientAdminViewSet
from django.urls import path, include
from recipes.views.step_viewset import StepViewSet, StepAdminViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)  # Registra el ViewSet de ingredientes
router.register(r'admin/ingredients', IngredientAdminViewSet)
router.register(r'steps', StepViewSet)
router.register(r'admin/steps', StepAdminViewSet)
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls

)),
]