from rest_framework import serializers
from measurements.models.unitType import UnitType
from rest_framework.exceptions import ValidationError

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
    # units = UnitSerializer(many=True, read_only=True)
    units = serializers.SerializerMethodField()

    class Meta:
        """
        Meta clase para definir metadatos del serializador UnitTypeSerializer.  
        """
        model = UnitType
        fields = ('name', 'units')
        read_only_fields = ('name', 'units')

    def get_units(self, obj):
        # We define a method to serialize the units. This allows us to import
        # UnitSerializer *inside* the method, avoiding circular dependency
        # during module loading.
        from measurements.serializers.unitSerializer import UnitSerializer
        return UnitSerializer(obj.units.all(), many=True, read_only=True).data

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

    units = serializers.SerializerMethodField()

    class Meta:
        model = UnitType
        fields = '__all__'
        read_only = True

    def get_units(self, obj):
        from measurements.serializers.unitSerializer import UnitAdminSerializer
        return UnitAdminSerializer(obj.units.all(), many=True, read_only=True).data

    def create(self, validated_data):
        raise ValidationError("This serializer is read-only; creation is not allowed.")

    def update(self, instance, validated_data):
        raise ValidationError("This serializer is read-only; updates are not allowed.")