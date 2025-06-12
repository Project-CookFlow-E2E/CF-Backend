from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from ..models.user import CustomUser
from ..serializers.userSerializer import (
    CustomUserSerializer,
    CustomUserAdminSerializer,
    CustomUserCreateSerializer,
    CustomUserLoginSerializer,
    CustomUserUpdateSerializer,
    CustomUserAdminUpdateSerializer
)
from ..models.favorite import Favorite
from ..serializers.favoriteSerializer import (
    FavoriteSerializer,
    FavoriteAdminSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    View para el registro de nuevos usuarios.
    Permite a cualquier usuario crear una nueva cuenta.
    Utiliza CustomUserCreateSerializer para la validación y creación.
    Args:
        generics.CreateAPIView: Clase base de DRF para vistas de creación.

    Attributes:
        queryset (CustomUser.objects.all()): Conjunto de objetos de usuario disponibles para esta vista.
        serializer_class (CustomUserCreateSerializer): Serializador utilizado para validar y crear nuevos usuarios.
        permission_classes (list): [AllowAny]: Permite el acceso a cualquier usuario, autenticado o no.
    Auth:
        Saturnino Mendez
    Modified by:  
        Ángel Aragón  
    Modified:
        - Agregada la lógica para devolver un error 409 (Conflict) si el error es por username o email duplicado.
        - Para otros errores de validación, responde con un error 400 (Bad Request).
        - Al crear un usuario exitosamente, devuelve el objeto creado con un código 201 (Created).
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            if 'username' in serializer.errors or 'email' in serializer.errors:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginView(APIView):
    """
    View para el inicio de sesión de usuarios.
    Permite a los usuarios autenticarse y obtener tokens JWT (Access y Refresh).
    Utiliza CustomUserLoginSerializer para la validación de credenciales.
    """
    permission_classes = [AllowAny]  # Access without auth

    def post(self, request, *_args, **_kwargs):
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # If auth fails, raises an exception

        user = serializer.validated_data.get("user")  # The serializer has already validated and got the user

        # Generate JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View para que un usuario autenticado vea y actualice su propio perfil.
    Acceso a: /users/me/ o /users/{pk}/
    """
    queryset = CustomUser.objects.all()  # It will be used for lookup, but get_object is overridden
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Garantiza que un usuario solo pueda ver/editar su propio perfil.
        Si la URL es /users/me/, devuelve el usuario autenticado.
        Si la URL es /users/{pk}/, verifica que el pk coincida con el usuario autenticado.
        """
        # For the URL /users/me/
        if self.kwargs.get('pk') == 'me':
            return self.request.user

        # For the URL /users/{pk}/, ensure the PK corresponds to the logged-in user
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if obj != self.request.user:
            self.permission_denied(
                self.request,
                message="No tienes permiso para acceder a este perfil."
            )
        return obj

    def get_serializer_class(self):
        """
        Devuelve el serializer adecuado según el tipo de petición (GET o PUT/PATCH).
        """
        if self.request.method == 'GET':
            return CustomUserSerializer  # To view the profile (read-only).
        return CustomUserUpdateSerializer  # To update the profile.


class AdminUserViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    Conjunto de Views para la gestión completa de usuarios por parte de un administrador.

    Args:
        generics.ListCreateAPIView: Proporciona las acciones `list` (listar todos los usuarios) y `create` (crear un nuevo usuario).
        generics.RetrieveUpdateDestroyAPIView: Proporciona las acciones `retrieve` (ver detalles de un usuario), `update` (actualizar un usuario existente) y `destroy` (eliminar un usuario).

    Attributes:
        `queryset`: `CustomUser.objects.all()`: El conjunto de objetos de usuario disponibles para esta vista.
        `permission_classes` (`list`): `[IsAdminUser]`: Define que solo los usuarios con `is_staff=True` (incluyendo superusuarios) pueden acceder a estas operaciones.

    Notas:
        Esta vista permite a los usuarios con permisos de administrador realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
        sobre todos los usuarios del sistema. Los serializers utilizados varían en función del tipo de petición
        (GET, POST, PUT/PATCH).
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]  # Only is_staff users can access

    def get_serializer_class(self):
        """
        Determina y devuelve el serializer adecuado para la acción solicitada.

        Args:
            self: La instancia de la vista.

        Returns:
            serializers.ModelSerializer: La clase del serializer a utilizar (CustomUserAdminSerializer,
            CustomUserCreateSerializer o CustomUserAdminUpdateSerializer) según el metodo de la petición.
        """
        if self.request.method == 'GET':
            return CustomUserAdminSerializer  # To list and view user details by admin
        elif self.request.method == 'POST':
            return CustomUserCreateSerializer  # To create a new user by admin (using the creation serializer)
        return CustomUserAdminUpdateSerializer  # To update users by admin


# Favorite views

class UserFavoriteListCreateView(generics.ListCreateAPIView):
    """
        Vista para que los usuarios autenticados listen y añadan sus propias recetas favoritas.

        Args:
            generics.ListCreateAPIView: Clase base de DRF para vistas de listado y creación.

        Attributes:
            `permission_classes` (`list`): `[IsAuthenticated]`: Solo usuarios autenticados.
            `serializer_class`: `FavoriteSerializer`: Serializador para la representación y creación de favoritos.

        Notas:
            Al crear un favorito, el usuario asociado se asigna automáticamente al usuario de la petición.
            La lista solo mostrará los favoritos del usuario actual.
        """
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        """
        Devuelve el queryset de favoritos, filtrado para mostrar solo los del usuario autenticado.
        """
        return Favorite.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        """
        Asigna automáticamente el usuario autenticado al campo `user_id` del nuevo favorito al crearlo.
        """
        serializer.save(user_id=self.request.user)


class UserFavoriteDestroyView(generics.DestroyAPIView):
    """
       Vista para que los usuarios autenticados eliminen sus propias recetas favoritas.

       Args:
           generics.DestroyAPIView: Clase base de DRF para vistas de eliminación.

       Attributes:
           `permission_classes` (`list`): `[IsAuthenticated]`: Solo usuarios autenticados.
           `serializer_class`: `FavoriteSerializer`: Serializador (no estrictamente necesario para DELETE, pero buena práctica).

       Notas:
           Se asegura que un usuario solo pueda eliminar sus propias recetas favoritas
           a través de la sobrescritura del metodo `get_queryset`.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        """
            Devuelve el queryset de favoritos, filtrado para asegurar que solo se puedan eliminar
            los favoritos pertenecientes al usuario autenticado.
        """
        return Favorite.objects.filter(user_id=self.request.user)


class AdminFavoriteViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
        Conjunto de vistas para la gestión completa de recetas favoritas por parte de un administrador.

        Args:
            generics.ListCreateAPIView: Proporciona las acciones `list` (listar todos los favoritos) y `create` (crear un nuevo favorito).
            generics.RetrieveUpdateDestroyAPIView: Proporciona las acciones `retrieve` (ver detalles de un favorito), `update` (actualizar un favorito existente) y `destroy` (eliminar un favorito).

        Attributes:
            `queryset`: `Favorite.objects.all()`: El conjunto completo de objetos de favoritos disponibles.
            `permission_classes` (`list`): `[IsAdminUser]`: Define que solo los usuarios con `is_staff=True` (incluyendo superusuarios) pueden acceder a estas operaciones.

        Notas:
            Esta vista permite a los usuarios con permisos de administrador realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
            sobre todas las recetas favoritas del sistema. Se utiliza `FavoriteAdminSerializer` para todas las operaciones de admin.
        """
    queryset = Favorite.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = FavoriteAdminSerializer
