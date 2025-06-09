from rest_framework.routers import DefaultRouter
from recipes.views.recipeView import RecipeViewSet
from recipes.views.ingredientViewSet import IngredientViewSet, IngredientAdminViewSet
from django.urls import path, include
from recipes.views.step_viewset import StepViewSet, StepAdminViewSet
from recipes.views.categoryView import CategoryView

router = DefaultRouter() 
router.register(r'ingredients', IngredientViewSet, basename='ingredient') 
router.register(r'admin/ingredients', IngredientAdminViewSet, basename='ingredient-admin') 
router.register(r'steps', StepViewSet, basename='step') 
router.register(r'admin/steps', StepAdminViewSet, basename='step-admin') 
router.register(r'recipes', RecipeViewSet, basename='recipe') 
router.register(r'categories', CategoryView, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]