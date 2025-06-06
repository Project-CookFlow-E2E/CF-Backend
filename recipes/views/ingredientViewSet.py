from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from recipes.models.ingredient import Ingredient
from recipes.serializers.ingredientSerializer import IngredientSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Ingredient.  

    
    Usuarios autenticados (IsAuthenticated) pueden realizar todas las operaciones CRUD.  
    Usuarios NO autenticados solo pueden hacer GET (listar ingredientes).,    


    Attributes:  
        queryset (QuerySet): Obtiene todos los objetos Ingredient.  
        serializer_class (IngredientSerializer): Serializer utilizado para manejar los datos.  
        permission_classes (list): Controla el acceso según autenticación.  

    Author:
        {Noemi Casaprima}
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # CRUD solo para autenticados, GET para todos

class IngredientAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Ingredient.

    Usuarios autenticados (IsAuthenticated) pueden realizar todas las operaciones CRUD.  
    Usuarios NO autenticados solo pueden hacer GET (listar ingredientes).,  

    Attributes:
        queryset (QuerySet): Obtiene todos los objetos Ingredient.  
        serializer_class (IngredientSerializer): Serializer utilizado para manejar los datos.  
        permission_classes (list): Solo accesible para usuarios administradores.  

    Author:
        {Noemi Casaprima}  
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminUser]