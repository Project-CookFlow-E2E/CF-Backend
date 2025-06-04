from django.conf import settings
from django.db import models
from measurements.models import UnitType


class Unit (models.Model):
    """Modelo de Unit, representa una unidad de medida o un tipo de unidad.  

    Args:  
        models (Model): Clase base de Django para modelos.  
    Attributes:  
        `name (str)`: Nombre de la unidad, debe ser único y tener una longitud máxima de 15 caracteres.  
        `created_at (DateTimeField)`: Fecha y hora de creación del registro, se establece automáticamente al crear el objeto.  
        `updated_at (DateTimeField)`: Fecha y hora de la última actualización del registro,
        se actualiza automáticamente al modificar el objeto.  
    `unit_type (ForeignKey)`: Relación con el modelo UnitType, que define el tipo de unidad.
    Author:  
    {Angel Aragón}
    """

    name = models.CharField(max_length=15, unique=True)
    unit_type = models.ForeignKey(settings.AUTH_UNITTYPE_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        """
        Meta clase para definir metadatos del modelo Unit.
        Esta clase define el nombre de la tabla en la base de datos.  
        Args:  
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'units'.
        """
        db_table = 'units'
