from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from recipes.models.step import Step
from recipes.serializers.stepSerializer import StepSerializer, StepAdminSerializer

class StepViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Step.

    Permite realizar operaciones CRUD en la API:
    - `GET /api/steps/` → Obtener todos los pasos.
    - `POST /api/steps/` → Crear un nuevo paso.
    - `GET /api/steps/{id}/` → Obtener un paso específico.
    - `PUT /api/steps/{id}/` → Actualizar un paso.
    - `DELETE /api/steps/{id}/` → Eliminar un paso.

    Attributes:
        queryset (QuerySet): Consulta sobre el modelo Step.
        serializer_class (StepSerializer): Serializer utilizado para manejar los datos.
        permission_classes = [IsAuthenticatedOrReadOnly]  # Permite GET a todos, pero CRUD solo a autenticados
    Author:
        {Rafael Fernández}
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Permite GET a todos, pero CRUD solo a autenticados

    def get_queryset(self):
        """
        Filtra los pasos para mostrar solo los que pertenecen a recetas específicas.
        """
        recipe_id = self.request.query_params.get('recipe_id')
        if recipe_id:
            return Step.objects.filter(recipe__id=recipe_id)
        return super().get_queryset()

class StepAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet administrativo para el modelo Step.

    Solo accesible para usuarios administradores y permite acceso completo a todos los datos de `Step`.

    Permite operaciones CRUD con restricciones en ciertos campos:
    - `GET /api/admin/steps/` → Lista todos los pasos con más detalles.
    - `POST /api/admin/steps/` → Crea un nuevo paso con información extendida.
    - `GET /api/admin/steps/{id}/` → Obtiene detalles completos de un paso.
    - `PUT /api/admin/steps/{id}/` → Actualiza un paso.
    - `DELETE /api/admin/steps/{id}/` → Elimina un paso.

    Attributes:
        queryset (QuerySet): Obtiene todos los pasos.
        serializer_class (StepAdminSerializer): Serializer con más información.
        permission_classes (list): Solo accesible para usuarios administradores.
    Author:
        {Rafael Fernández}
    """
    queryset = Step.objects.all()
    serializer_class = StepAdminSerializer
    permission_classes = [IsAdminUser]
