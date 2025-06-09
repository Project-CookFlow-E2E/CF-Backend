from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from recipes.models.recipe import Recipe
from recipes.serializers.recipeSerializer import RecipeSerializer, RecipeAdminSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Recipe.

    Usuarios autenticados pueden realizar todas las operaciones CRUD.
    Usuarios NO autenticados solo pueden hacer GET (listar y ver recetas).

    Attributes:
        queryset (QuerySet): Obtiene todos los objetos Recipe.
        permission_classes (list): Controla el acceso según autenticación.
        get_serializer_class (func): Selecciona el serializer según el tipo de usuario.

    Author:
        {Lorena Martínez}
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return RecipeAdminSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)








