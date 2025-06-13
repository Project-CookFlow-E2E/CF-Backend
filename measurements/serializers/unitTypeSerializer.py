from rest_framework import serializers
from measurements.models import UnitType
from .unitSerializer import UnitSerializer

class UnitTypeSerializer(serializers.ModelSerializer):

    """
    Serializer para el modelo UnitType.  
    Este serializador se utiliza para convertir instancias del modelo UnitType
    en representaciones JSON y viceversa.  
    Attributes:  
        - `model (Model)`: El modelo al que se aplica el serializador.  
        - `fields (tuple)`: Los campos del modelo que se incluirán en la representación JSON.  
        - `read_only_fields (tuple)`: Los campos que son de solo lectura y no se pueden modificar.  
    Args:
        serializers (serializers.ModelSerializer): Clase base de Django para serializadores.  
    Author:  
        {Angel Aragón}
    """
    units = UnitSerializer(many=True, read_only=True)
    class Meta:
        """
        Meta clase para definir metadatos del serializador UnitTypeSerializer.  
        """
        model = UnitType
        fields = ('name', 'units')
        read_only_fields = ('name', 'units')

class UnitTypeAdminSerializer(serializers.ModelSerializer):
    """Serializer para el modelo UnitType en el panel de administración.
    Este serializador se utiliza para convertir instancias del modelo UnitType
    en representaciones JSON y viceversa.  
    Attributes:  
        - `model (Model)`: El modelo al que se aplica el serializador.  
        - `fields (tuple)`: Los campos del modelo que se incluirán en la representación JSON.  
        - `read_only_fields (tuple)`: Los campos que son de solo lectura y no se pueden modificar.
        - `extra_kwargs (dict)`: Campos adicionales con restricciones específicas, como longitud máxima.  
    Args:  
        serializers (serializers.ModelSerializer): Clase base de Django para serializadores.
    Author:  
        {Angel Aragón}  
    """
    class Meta:
        model = UnitType
        fields = ('name', 'units')
        read_only_fields = ('name', 'units')
        extra_kwargs = {
            'name': {'required': True, 'max_length': 15},
        }