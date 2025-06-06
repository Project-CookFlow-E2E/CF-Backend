from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.user import CustomUser
from ..serializers.userSerializer import (
    CustomUserSerializer,
    CustomUserAdminSerializer,
    CustomUserCreateSerializer,
    CustomUserLoginSerializer,
    CustomUserUpdateSerializer,
    CustomUserAdminUpdateSerializer
)

class UserRegistrationView(generics.GenericAPIView):
    """
    View para el registro de nuevos usuarios.
    Permite a cualquier usuario crear una nueva cuenta.
    Utiliza CustomUserCreateSerializer para la validación y creación.

    Auth:
        Saturnino Mendez
    """
    queryset = CustomUser.objects.all()
    serializer_class =  CustomUserCreateSerializer
    permission_classes =  [AllowAny] # Access without auth

class UserLoginView(APIView):
    """
    View para el inicio de sesión de usuarios.
    Permite a los usuarios autenticarse y obtener tokens JWT (Access y Refresh).
    Utiliza CustomUserLoginSerializer para la validación de credenciales.
    """
    permission_classes = [AllowAny] # Access without auth

    def post(self, request, *args, **kwargs):
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) # If auth fails, raises an exception

        user = serializer.validated_data.get("user") # The serializer has already validated and got the user

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
    queryset = CustomUser.objects.all() # It will be used for lookup, but get_object is overridden
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
        obj = generics._get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
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
            return CustomUserSerializer # To view the profile (read-only).
        return CustomUserUpdateSerializer # To update the profile.

class AdminUserViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    Conjunto de Views para la gestión de usuarios por parte de un administrador.
    Permite a los usuarios is_staff listar, crear, ver, actualizar y eliminar usuarios.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser] # Only is_staff users can access

    def get_serializer_class(self):
        """
        Devuelve el serializer adecuado según la acción (list/retrieve, create, update).
        """
        if self.request.method == 'GET':
            return CustomUserAdminSerializer # To list and view user details by admin
        elif self.request.method == 'POST':
            return CustomUserCreateSerializer # To create a new user by admin (using the creation serializer)
        return CustomUserAdminUpdateSerializer # To update users by admin

# Favorite views
#Es necesario hacer 1 para que el usuario estandar pueda ver y eliminar los suyos y otro para el admin con esto mismo y los de los demás.