from django.conf import settings
from django.db import models
from .unitType import UnitType

class Unit (models.Model):
    """Modelo de Unit, representa una unidad de medida o un tipo de unidad.  

    Args:  
        models (Model): Clase base de Django para modelos.  
    Attributes:  
        -`name (str)`: Nombre de la unidad, debe ser único y tener una longitud máxima de 15 caracteres.  
        -`created_at (DateTimeField)`: Fecha y hora de creación del registro, se establece automáticamente al crear el objeto.  
        -`unit_type (ForeignKey)`: Relación con el modelo UnitType, que define el tipo de unidad.  
        -`user_id (ForeignKey)`: Relación con el modelo de usuario, que indica quién creó la unidad.
    Author:  
    {Angel Aragón}
    """

    name = models.CharField(max_length=15, unique=True)
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE, related_name='units') 
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        
        """
        Meta clase para definir metadatos del modelo Unit.
        Esta clase define el nombre de la tabla en la base de datos.  
        Args:  
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'units'.
        """
        db_table = 'units'
