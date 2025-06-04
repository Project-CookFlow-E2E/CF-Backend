from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
	"""
	Gestor personalizado para el modelo CustomUser.

	Contiene métodos para crear usuarios normales y superusuarios utilizando
	los mecanismos integrados de Django (is_superuser, is_staff).

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
			password (str, optional): Contraseña del superusuario.
			extra_fields (dict): Campos adicionales opcionales.

		Returns:
			CustomUser: El superusuario creado.
		"""
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_staff', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('El superusuario debe tener is_superuser=True.')
		if extra_fields.get('is_staff') is not True:
			raise ValueError('El superusuario debe tener is_staff=True.')

		return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
	"""
	Modelo personalizado de usuario para la tabla 'users'.

	Aprovecha AbstractBaseUser y PermissionsMixin para un control total
	sobre la autenticación y los permisos.

	Attributes:
		username (str): Nombre de usuario.
		email (str): Email del usuario.
		name (str): Nombre de pila del usuario.
		surname (str): Primer apellido del usuario.
		second_surname (str): Segundo apellido del usuario.
		biography (str): Biografía mostrada en el perfil del usuario.
		is_staff (bool): Define si el usuario puede acceder al admin.
		created_at (DateTimeField): Fecha de creación del registro.
		updated_at (DateTimeField): Fecha de última actualización del registro.
	"""

	username = models.CharField(max_length=255, unique=True, null=False)
	email = models.EmailField(max_length=50, null=False, unique=True)
	name = models.CharField(max_length=50, null=False)
	surname = models.CharField(max_length=50, null=False)
	second_surname = models.CharField(max_length=50, null=False)
	biography = models.CharField(max_length=100, null=True, blank=True)
	is_staff = models.BooleanField(default=False)
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
