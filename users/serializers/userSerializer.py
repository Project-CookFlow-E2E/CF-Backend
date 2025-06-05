from rest_framework import serializers
from ..models.user import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    	Serializer del modelo CustomUser para usuarios estandar.

    	Este serializer transforma instancias del modelo CustomUser en representaciones JSON
    	y viceversa. Incluye los campos relevantes para mostrar información del usuario en el frontend.

    	Fields:
    		id: ID del usuario.
    		username: Nombre de usuario único.
    		email: Dirección de correo electrónico.
    		name: Nombre de pila.
    		surname: Primer apellido.
    		second_surname: Segundo apellido.
    		biography: Breve descripción del usuario.
    		created_at: Fecha de creacion del usuario.
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
    	Serializer del modelo CustomUser para usuarios is_staff.

    	Este serializer transforma instancias del modelo CustomUser en representaciones JSON
    	y viceversa. Incluye los campos relevantes para mostrar información del usuario en el frontend.

    	Fields:
    	    id: ID del usuario.
    		username – Nombre de usuario.
            email – Email del usuario.
            password - Contraseña del usuario.
            name – Nombre de pila del usuario.
            surname – Primer apellido del usuario.
            second_surname – Segundo apellido del usuario.
            biography – Biografía mostrada en el perfil del usuario.
            is_staff – Define si el usuario puede acceder al admin.
            created_at – Fecha de creación del registro.
            updated_at – Fecha de última actualización del registro.
    	"""

    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """
        Serializer del modelo CustomUser para la creación de usuarios estándar.

        Este serializer se encarga de transformar instancias del modelo CustomUser
        en representaciones JSON y viceversa. Se utiliza específicamente para la
        creación de nuevos usuarios, incluyendo la gestión de la contraseña.

        Campos:
            username (str): Nombre de usuario.
            email (str): Dirección de correo electrónico del usuario.
            password (str): Contraseña del usuario (solo escritura).
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

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        # user.set_password(password)
        user.save()
        return user


class CustomUserLoginSerializer(serializers.Serializer):
    """
    Serializer que permite iniciar sesión con username o email.
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
    	Serializer que permite actualizar los datos del usuario estandar.
    	"""

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'second_surname', 'biography', 'password']

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
        Serializer que permite actualizar los datos del usuario estandar y is_staff al usuario is_staff.
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
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        #if password:
            #instance.set_password(password)
        instance.save()
        return instance
