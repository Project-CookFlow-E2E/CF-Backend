from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from recipes.models import Category
from recipes.serializers.categorySerializer import (
    CategorySerializer,
    CategoryAdminSerializer,
)


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
        queryset = Category.objects.all()  # Trae todas las categorías
        
        parent_category_id = self.request.query_params.get("parent_category_id")  # Obtiene el valor del parámetro
        if parent_category_id is not None:
            queryset = queryset.filter(parent_category_id=parent_category_id)  # Filtra por parent_category_id
        
        return queryset
    
    def get_permissions(self):
        """
        Define los permisos de acceso según el método de la solicitud.

        Returns:
            list: Lista con la clase de permisos correspondiente.
        """
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]  # Solo los administradores pueden hacer cambios (POST, PUT, DELETE)
        return [IsAuthenticatedOrReadOnly()]  # Los usuarios autenticados pueden leer (GET) y no modificar
    
    def get_serializer_class(self):
        """
        Determina el serializador a utilizar según el estado del usuario.

        Returns:
            Serializer: Serializador adecuado para el usuario.
        """
        if self.request.user.is_staff:
            return CategoryAdminSerializer
        return CategorySerializer
