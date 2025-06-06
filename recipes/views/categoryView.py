from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from recipes.models import Category
from recipes.serializers.categorySerializer import CategorySerializer, CategoryAdminSerializer

class CategoryView(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías en la aplicación de recetas.

    Métodos:
        - get_queryset: Devuelve todas las categorías disponibles.
        - get_permissions: Define los permisos según el método de la solicitud.
        - get_serializer_class: Determina el serializador a utilizar basado en si el usuario es administrador o no.

    Autor: Ana Castro
    """

    def get_queryset(self):
        """
        Obtiene el conjunto de categorías disponibles.

        Returns:
            QuerySet: Todas las instancias de la clase Category.
        """
        return Category.objects.all()

    def get_permissions(self):
        """
        Define los permisos de acceso según el método de la solicitud.

        Returns:
            list: Lista con la clase de permisos correspondiente.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        """
        Determina el serializador a utilizar según el estado del usuario.

        Returns:
            Serializer: Serializador adecuado para el usuario.
        """
        if self.request.user.is_staff:
            return CategoryAdminSerializer
        return CategorySerializer
