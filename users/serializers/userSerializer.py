from rest_framework import serializers
from ..models.user import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer del modelo CustomUser para usuarios estándar (solo lectura).

    Este serializer transforma instancias del modelo CustomUser en representaciones JSON
    para ser mostradas en el frontend. Está diseñado para la visualización pública
    o estándar de la información del usuario, excluyendo datos sensibles como la contraseña.

    Campos:
       id: ID único del usuario.
       username: Nombre de usuario único para inicio de sesión.
       email: Dirección de correo electrónico del usuario.
       name: Nombre de pila del usuario.
       surname: Primer apellido del usuario.
       second_surname: Segundo apellido del usuario.
       biography: Breve descripción o biografía del usuario.
       created_at: Fecha y hora de creación del registro del usuario.
    """

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'name',
            'surname',
            'second_surname',
            'biography',
            'created_at'
        ]
        read_only_fields = fields


class CustomUserAdminSerializer(serializers.ModelSerializer):
    """
    Serializer del modelo CustomUser para la visualización y gestión por parte de usuarios `is_staff`.

    Este serializer transforma instancias del modelo CustomUser en representaciones JSON
    y viceversa, permitiendo a los administradores ver y potencialmente modificar todos los
    campos del usuario, excepto los campos de solo lectura definidos.
    Aunque incluye 'password' en '__all__', este campo no se serializará en la salida
    debido a que Django ya lo gestiona hasheado internamente y no es un campo de modelo
    directamente legible en texto plano. Se asume que la modificación de la contraseña
    se realizará a través de un serializer de actualización específico.

    Campos:
        id: ID único del usuario.
        username: Nombre de usuario.
        email: Email del usuario.
        password: Contraseña del usuario (no es un campo de lectura directa, solo para operaciones internas).
        name: Nombre de pila del usuario.
        surname: Primer apellido del usuario.
        second_surname: Segundo apellido del usuario.
        biography: Biografía mostrada en el perfil del usuario.
        is_staff: Define si el usuario tiene acceso al panel de administración.
        created_at: Fecha de creación del registro.
        updated_at: Fecha de última actualización del registro.
    """

    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer del modelo CustomUser para la creación de nuevos usuarios estándar.

    Este serializer se encarga de transformar los datos de entrada JSON en instancias
    del modelo CustomUser, gestionando específicamente el hasheo y almacenamiento
    seguro de la contraseña del nuevo usuario.

    Campos:
        username (str): Nombre de usuario único.
        email (str): Dirección de correo electrónico del usuario.
        password (str): Contraseña del usuario (campo de solo escritura).
        name (str): Nombre de pila del usuario.
        surname (str): Primer apellido del usuario.
        second_surname (str): Segundo apellido del usuario.
        biography (str): Biografía mostrada en el perfil del usuario.
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'name',
            'surname',
            'second_surname',
            'biography',
            'password'
        ]

    def validate_password(self, value):
        """
        Valida la fortaleza de la contraseña usando los validadores configurados en Django settings.
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        # user.set_password(password)
        user.save()
        return user


class CustomUserLoginSerializer(serializers.Serializer):
    """
    Serializer para el proceso de inicio de sesión.

    Este serializer maneja la validación de las credenciales de un usuario,
    permitiendo el inicio de sesión tanto con el nombre de usuario como con el correo electrónico.
    Verifica la contraseña hasheada y el estado de actividad del usuario.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_input = data.get("username")
        password = data.get("password")

        user_obj = CustomUser.objects.filter(email=user_input).first() or CustomUser.objects.filter(
            username=user_input).first()

        if user_obj and user_obj.check_password(password):
            if not user_obj.is_active:
                raise serializers.ValidationError("Usuario inactivo.")
            data["user"] = user_obj
            return data

        raise serializers.ValidationError("Credenciales inválidas.")


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para la actualización de datos de un usuario estándar.

    Este serializer se encarga de transformar los datos de entrada JSON en instancias
    del modelo CustomUser, permitiendo la modificación de campos específicos por parte
    del propio usuario o un proceso similar, incluyendo la actualización opcional de la contraseña.
    """

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'second_surname', 'biography', 'password']

    def validate_password(self, value):
        """
        Valida la fortaleza de la contraseña usando los validadores configurados en Django settings.
        Este método se ejecuta solo si se proporciona una nueva contraseña.
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # if password:
        # instance.set_password(password)
        instance.save()
        return instance


class CustomUserAdminUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para la actualización de datos de cualquier usuario por parte de un usuario `is_staff`.

    Este serializer se encarga de transformar los datos de entrada JSON en instancias
    del modelo CustomUser, permitiendo a un administrador modificar la información de
    cualquier usuario, incluyendo su estado de `is_staff` y la actualización opcional de la contraseña.
    """

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'name', 'surname',
            'second_surname', 'biography', 'is_staff', 'password'
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        """
        Valida la fortaleza de la contraseña usando los validadores configurados en Django settings.
        Este método se ejecuta solo si se proporciona una nueva contraseña.
        """

        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
