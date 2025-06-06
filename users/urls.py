from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views.userView import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    AdminUserViewSet,
    UserFavoriteListCreateView,
    UserFavoriteDestroyView,
    AdminFavoriteViewSet
)

"""
Definición de las rutas de API para la gestión de usuarios y recetas favoritas.

Este módulo mapea las URLs a las vistas correspondientes dentro de la aplicación 'users'.
Define los endpoints para el registro, inicio de sesión, gestión de perfiles de usuario
y operaciones CRUD sobre las recetas favoritas, tanto para usuarios autenticados como
para administradores.

Attributes:
    `urlpatterns` (`list`): Una lista de objetos `path` que asocian patrones de URL
    con las vistas de Django REST Framework (DRF). Incluye rutas para:
        - Autenticación de usuarios (registro, login, tokens JWT).
        - Gestión de perfiles de usuario (propios y por ID).
        - Gestión de usuarios por parte de administradores.
        - Gestión de recetas favoritas por parte de usuarios autenticados.
        - Gestión de recetas favoritas por parte de administradores.

Notas:
    - Las rutas `/token/` y `/token/refresh/` son proporcionadas por `rest_framework_simplejwt`
      para la obtención y renovación de tokens de acceso JWT.
    - Se utilizan prefijos como `users/` y `favorites/` para organizar los endpoints
      relacionados con cada recurso.
    - Las rutas para administradores (`admin/users/` y `admin/favorites/`) requieren
      permisos específicos (`IsAdminUser`).
      
Auth:
    Saturnino Mendez
"""

urlpatterns = [
    #Auth and user routes
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/me/', UserProfileView.as_view(), name='user-profile-me'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile-detail'),

    #User administration routes
    path('admin/users/', AdminUserViewSet.as_view(), name='admin-user-list-create'),
    path('admin/users/<int:pk>/', AdminUserViewSet.as_view(), name='admin-user-detail-update-destroy'),

    #Favorite routes for auth user
    path('favorites/', UserFavoriteListCreateView.as_view(), name='user-favorite-list-create'),
    path('favorites/<int:pk>/', UserFavoriteDestroyView.as_view(), name='user-favorite-destroy'),

    #Routes for favorites administration
    path('admin/favorites', AdminFavoriteViewSet.as_view(), name='admin-favorite-list-create'),
    path('admin/favorites/<int:pk>/', AdminFavoriteViewSet.as_view(), name='admin-favorite-detail-update-destroy'),

    #Routes for get and refresh JWT tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obatin_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]