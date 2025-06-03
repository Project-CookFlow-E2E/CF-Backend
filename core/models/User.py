from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
	"""
	Gestor personalizado para el modelo CustomUser.

	Contiene métodos para crear usuarios normales y administradores sin usar
	los campos por defecto del modelo User de Django.

	Methods:
		create_user(username, email, password, **extra_fields):
			Crea y guarda un usuario con los campos dados.
		create_superuser(username, email, password, **extra_fields):
			Crea y guarda un superusuario con permisos administrativos.
	"""

	def create_user(self, username, email, password=None, **extra_fields):
		"""
		Crea y guarda un usuario con el nombre de usuario, email y contraseña dados.

		Args:
			username (str): Nombre de usuario.
			email (str): Dirección de correo electrónico.
			password (str, optional): Contraseña del usuario.
			extra_fields (dict): Campos adicionales opcionales.

		Returns:
			CustomUser: El usuario creado.
		"""
		if not email:
			raise ValueError('El email es obligatorio')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password=None, **extra_fields):
		"""
		Crea y guarda un superusuario con permisos administrativos.

		Args:
			username (str): Nombre de usuario.
			email (str): Dirección de correo electrónico.
			password (str, optional): Contraseña del usuario.
			extra_fields (dict): Campos adicionales opcionales.

		Returns:
			CustomUser: El superusuario creado.
		"""
		extra_fields.setdefault('is_admin', True)
		return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
	"""
	Modelo de la tabla users

	Args:
		AbstractBaseUser (class): Clase base para definir modelos personalizados de usuario.
		PermissionsMixin (class): Mezcla para incluir soporte a permisos y grupos.

	Attributes:
		username (str): Nombre de usuario
		email (str): Email del usuario
		name (str): Nombre de pila del usuario
		surname (str): Primer apellido del usuario
		second_surname (str): Segundo apellido del usuario
		is_admin (bool): Determina si es administrador o no el usuario
		biography (str): Biografía que se muestra en la página de perfil del usuario
		created_at (DateTimeField): Fecha y hora de creación del registro, se establece automáticamente al crearlo
		updated_at (DateTimeField): Fecha y hora de la última actualización del registro, se actualiza automáticamente al modificarlo

	Author:
		Saturnino Méndez
	"""
	username = models.CharField(max_length=255, unique=True, null=False)
	email = models.EmailField(max_length=50, null=False, unique=True)
	name = models.CharField(max_length=50, null=False)
	surname = models.CharField(max_length=50, null=False)
	second_surname = models.CharField(max_length=50, null=False)
	is_admin = models.BooleanField(default=False, null=False)
	biography = models.CharField(max_length=100, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'name', 'surname']

	class Meta:
		"""
		Configuración meta para el modelo CustomUser.

		Attributes:
			db_table (str): Nombre personalizado de la tabla en la base de datos ('users').
		"""
		db_table = 'users'
