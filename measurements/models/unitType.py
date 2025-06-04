from django.db import models
class UnitType(models.Model):
    """
    Modelo de UnitType, representa un tipo de unidad de medida.

    Args:
        models (Model): Clase base de Django para modelos.

    Attributes:
        name (str): Nombre del tipo de unidad, debe ser único y tener una longitud máxima de 15 caracteres.
        created_at (DateTimeField): Fecha y hora de creación del registro, se establece automáticamente al crear el objeto.
    """
    name = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta clase para definir metadatos del modelo UnitType.
        Esta clase define el nombre de la tabla en la base de datos.

        Args:
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'unit_types'.
        """
        db_table = 'unit_types'

    
