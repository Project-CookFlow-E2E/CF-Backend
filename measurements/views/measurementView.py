"""Este módulo contiene las vistas para manejar las operaciones CRUD de las unidades de medida y tipos de unidades.  

Estas vistas utilizan Django REST Framework para proporcionar una API RESTful que permite a los usuarios interactuar con los modelos `Unit` y `UnitType`.  
Las vistas están diseñadas para ser utilizadas por administradores y permiten la creación, actualización, eliminación y consulta de unidades de medida y tipos de unidades.  

Author:  
    {Angel Aragón}
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType
from measurements.serializers.unitSerializer import UnitSerializer, UnitAdminSerializer
from measurements.serializers.unitTypeSerializer import UnitTypeSerializer, UnitTypeAdminSerializer

class UnitViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar las operaciones CRUD de las unidades de medida. 
    Args:  
        - `viewsets (ModelViewSet)`: Clase base de Django REST Framework para manejar vistas basadas en conjuntos de datos.  
    Attributes:  
        - `queryset (QuerySet)`: Conjunto de datos que contiene todas las unidades de medida.  
    Returns:  
        - `UnitViewSet`: Un conjunto de vistas que permite realizar operaciones CRUD sobre el modelo Unit.   
    """
    queryset = Unit.objects.all()

    def get_serializer_class(self):
        """Determina qué clase de serializador usar según el método HTTP y los permisos del usuario.
        Si el método no es seguro (POST, PUT, PATCH, DELETE) y el usuario es staff, se usa el serializador de administrador.
        """
        if self.request.method not in SAFE_METHODS and self.request.user and self.request.user.is_staff:
            return UnitAdminSerializer
        return UnitSerializer

    def get_permissions(self):
        """Determina los permisos necesarios para acceder a la vista.
        Si el método es seguro (GET, HEAD, OPTIONS), no se requieren permisos especiales.
        """
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]

class UnitTypeViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar las operaciones CRUD de los tipos de unidades.
    Args:  
        - `viewsets (ModelViewSet)`: Clase base de Django REST Framework para manejar vistas basadas en conjuntos de datos.
    Attributes:
        - `queryset (QuerySet)`: Conjunto de datos que contiene todos los tipos de unidades.
    Returns:  
        - `UnitTypeViewSet`: Un conjunto de vistas que permite realizar operaciones CRUD sobre el modelo UnitType.
    """
    queryset = UnitType.objects.all()

    def get_serializer_class(self):
        """Determina qué clase de serializador usar según el método HTTP y los permisos del usuario.
        Si el método no es seguro (POST, PUT, PATCH, DELETE) y el usuario es staff, se usa el serializador de administrador.
        """
        if self.request.method not in SAFE_METHODS and self.request.user and self.request.user.is_staff:
            return UnitTypeAdminSerializer
        return UnitTypeSerializer

    def get_permissions(self):
        """Determina los permisos necesarios para acceder a la vista.
        Si el método es seguro (GET, HEAD, OPTIONS), no se requieren permisos especiales.
        """
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]