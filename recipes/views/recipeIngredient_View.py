from rest_framework import generics
from recipes.models.recipe_ingredient import RecipeIngredient
from recipes.serializers.recipe_ingredient_serializer import RecipeIngredientSerializer


class RecipeIngredientListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista todos los ingredientes de recetas.
    POST: Crea un nuevo ingrediente asociado a una receta.
    """
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


class RecipeIngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Obtiene un ingrediente específico de una receta.
    PUT/PATCH: Actualiza la cantidad o unidad.
    DELETE: Elimina la relación ingrediente-receta.
    """
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
