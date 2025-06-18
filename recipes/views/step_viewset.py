# recipes/views/step_viewset.py

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from recipes.models.step import Step
from recipes.serializers.stepSerializer import StepSerializer, StepAdminSerializer
from media.services.image_service import update_image_for_instance

class StepViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet para el modelo Step.

    Permite listar, obtener detalles, actualizar y eliminar pasos existentes.
    La creación de pasos se gestiona EXCLUSIVAMENTE a través del endpoint de la Receta.
    ...
    """
    queryset = Step.objects.all()

    def get_serializer_class(self):
        """
        Usa StepAdminSerializer si el usuario es staff y la solicitud no es segura (PUT, PATCH, DELETE).
        Usa StepSerializer para todas las demás solicitudes (GET).
        """
        if self.request.method not in SAFE_METHODS and self.request.user and self.request.user.is_staff:
            return StepAdminSerializer
        return StepSerializer

    def get_permissions(self):
        """
        Permite `GET` a todos los usuarios.
        Para `PUT`, `PATCH` y `DELETE`, exige que el usuario esté autenticado.
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

    def perform_update(self, serializer):
        step = serializer.save()
        image_file = self.request.FILES.get("step_image")
        if image_file:
            update_image_for_instance(
                image_file=image_file,
                user_id=self.request.user.id,
                external_id=step.id,
                image_type="STEP"
            )


class StepAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet administrativo para el modelo Step.
    """
    queryset = Step.objects.all()
    serializer_class = StepAdminSerializer
    permission_classes = [IsAdminUser]