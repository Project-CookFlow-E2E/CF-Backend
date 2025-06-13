from rest_framework import serializers
from measurements.models.unit import Unit
from rest_framework.exceptions import ValidationError

class UnitSerializer(serializers.ModelSerializer):
    """  
    Serializador para el modelo Unit.
    Este serializador se utiliza para convertir instancias del modelo Unit
    en representaciones JSON y viceversa.  
    Attributes:  
        -`model (Model)`: El modelo al que se aplica el serializador.  
        -`fields (tuple)`: Los campos del modelo que se incluirán en la representación JSON.  
        -`read_only_fields (tuple)`: Los campos que son de solo lectura y no se pueden modificar. 
    Args:  
        serializers (serializers.ModelSerializer): Clase base de Django para serializadores.  
    Author:  
    {Angel Aragón}
    """
    class Meta:
        """
        Meta información para el serializador Unit.
        """
        model = Unit
        fields = ('name', 'unit_type')
        read_only_fields = ('name', 'unit_type')

class UnitAdminSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Unit en el panel de administración.  
    Este serializador se utiliza para convertir instancias del modelo Unit
    en representaciones JSON y viceversa.  
    Attributes:  
        -`model (Model)`: El modelo al que se aplica el serializador.  
        -`fields (tuple)`: Los campos del modelo que se incluirán en la representación JSON.  
        -`read_only_fields (tuple)`: Los campos que son de solo lectura y no se pueden modificar.  
        -`extra_kwargs (dict)`: Campos adicionales con restricciones específicas, como longitud máxima.  
    Args:  
        serializers (serializers.ModelSerializer): Clase base de Django para serializadores.  
    Author:  
    {Angel Aragón}
    """
    class Meta:
        """
        Meta información para el serializador UnitAdmin.
        """
        model = Unit
        fields = '__all__'
        read_only = True

    def create(self, validated_data):
        raise ValidationError("This serializer is read-only; creation is not allowed.")

    def update(self, instance, validated_data):
        raise ValidationError("This serializer is read-only; updates are not allowed.")