from django.db import models

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
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    second_surname = models.CharField(max_length=50, null=False)
    is_admin = models.BooleanField(default=False, null=False)
    biography = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Configuración meta para el modelo CustomUser.

        Attributes:
            db_table (str): Nombre personalizado de la tabla en la base de datos ('users').
        """
        db_table = 'users'