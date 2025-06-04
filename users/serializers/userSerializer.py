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
        read_only_fields = ['id','created_at', 'updated_at']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',

        ]