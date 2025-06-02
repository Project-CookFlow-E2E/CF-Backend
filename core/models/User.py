from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    """
           Crea y guarda un nuevo usuario con los datos proporcionados.

           Args:
               username (str): Nombre de usuario. Obligatorio.
               email (str): Correo electrónico. Obligatorio.
               surname (str): Primer apellido. Obligatorio.
               second_surname (str): Segundo apellido. Obligatorio.
               password (str, optional): Contraseña del usuario.
               **extra_fields: Campos adicionales opcionales.

           Raises:
               ValueError: Si no se proporciona username o email.

           Returns:
               CustomUser: El usuario recién creado.

           Author:
                Saturnino Méndez
           """
    def create_user(self, username, email, surname, second_surname, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        if not email:
            raise ValueError('El correo electrónico es obligatorio')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            surname=surname,
            second_surname=second_surname,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

class CustomUser(models.Model):
    """
        Modelo de la tabla users

        Args:
            models (Model): Clase base de Django para modelos.

        Attributes:
            username (str): Nombre de usuario
            email (str): Email del usuario
            surname (str): Primer apellido del usuario
            second_surname (str): Segundo apellido del usuario
            is_admin (bool): Determina si es administrador o no el usuario
            biography (str): Biografia que se muestra en la página de perfil del usuario
            created_at (DateTimeField): Fecha y hora de creación del registro, se establece automáticamente al modificar el objeto
            updated_at (DateTimeField): Fecha y hora de la última actualización del registro, se actualiza automáticamente al modificar el objeto

        Author:
            Saturnino Méndez

        """
    username = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    surname = models.CharField(max_length=50, null=False)
    second_surname = models.CharField(max_length=50, null=False)
    is_admin = models.BooleanField(default=False, null=False)
    biography = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'surname', 'second_surname']

    class Meta:
        """
        Configuración meta para el modelo CustomUser.

        Attributes:
            db_table (str): Nombre personalizado de la tabla en la base de datos ('users').
        """
        db_table = 'users'