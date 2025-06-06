from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly, IsAdminUser, SAFE_METHODS
from recipes.models.step import Step
from recipes.serializers.stepSerializer import StepSerializer, StepAdminSerializer

class StepViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Step.

    - Usuarios autenticados pueden realizar todas las operaciones CRUD.
    - Usuarios no autenticados solo pueden hacer `GET` (listar pasos).

    Attributes:
        queryset (QuerySet): Obtiene todos los objetos Step.
        serializer_class (StepSerializer): Serializador para manejar los datos.
        permission_classes (list): Controla el acceso según autenticación.
    
    Author:
        {Rafael Fernández}
    """
    queryset = Step.objects.all()

    def get_serializer_class(self):
        """
        Usa StepAdminSerializer si el usuario es staff y la solicitud no es segura (`POST`, `PUT`, `DELETE`).
        Usa StepSerializer para todas las demás solicitudes (`GET`).
        """
        if self.request.method not in SAFE_METHODS and self.request.user and self.request.user.is_staff:
            return StepAdminSerializer
        return StepSerializer

    def get_permissions(self):
        """
        Permite `GET` a todos los usuarios.
        Para `POST`, `PUT` y `DELETE`, exige que el usuario esté autenticado.
        """
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """
        Filtra los pasos por receta si se pasa `recipe_id` como parámetro.
        """
        recipe_id = self.request.query_params.get('recipe_id')
        if recipe_id:
            return Step.objects.filter(recipe__id=recipe_id)
        return super().get_queryset()

class StepAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet administrativo para el modelo Step.

    - Solo accesible para administradores (`IsAdminUser`).
    - Permite acceso completo a `Step`, incluyendo operaciones CRUD.

    Attributes:
        queryset (QuerySet): Obtiene todos los objetos Step.
        serializer_class (StepAdminSerializer): Serializer con información extendida.
        permission_classes (list): Solo accesible para usuarios administradores.
    
    Author:
        {Rafael Fernández}
    """
    queryset = Step.objects.all()
    serializer_class = StepAdminSerializer
    permission_classes = [IsAdminUser]
