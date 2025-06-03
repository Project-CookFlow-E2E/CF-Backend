from django.db import models

class Image(models.Model):
    """Modelo de Image, representa una imagen almacenada.  

    Args:  
        models (Model): Clase base de Django para modelos.  
    Attributes:  
        `name (str)`: Nombre de la imagen con el hash, debe ser único y tener una longitud máxima de 100 caracteres.  
        `url (str)`: Url de la imagen, debe ser únicoa y tener una longitud máxima de 100 caracteres.  
        `processing_status (Choice)`: Incica el status de procesamiento de la imagen y los valores que admite son [UPLOADED, PROCESSING, COMPLETED, FAILED].
        `type (Choice)`: Incica el tipo de tabla a la que tiene que esta asociada la imagen y los valores que admite son [USER, RECIPE, STEP].
        `external_id (AutoField)`: Id de la tabla externa a la que hace referencia la imagen.
        `created_at (DateTimeField)`: Fecha y hora de creación del registro, se establece automáticamente al crear el objeto.  
    Author:  
    {Jose Barreiro}
    """
    class ImageType(models.TextChoices):
        USER = 'USER', 'User', 'user'
        RECIPE = 'RECIPE', 'Recipe', 'recipe'
        STEP = 'STEP', 'Step', 'step'
    class ImageStatus(models.TextChoices):
        UPLOADED = 'UPLOADED', 'Uploaded', 'uploaded'
        PROCESSING = 'PROCESSING', 'Processing', 'processing'
        COMPLETED = 'COMPLETED', 'Completed', 'completed'
        FAILED = 'FAILED', 'Failed', 'failed'
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=15,
        choices=ImageType.choices
    )
    url = models.CharField(max_length=100)
    processing_status = models.CharField(
        max_length=15,
        choices=ImageType.choices,
        default="uploaded"
    )
    external_id = models.AutoField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta clase para definir metadatos del modelo Image.
        Esta clase define el nombre de la tabla en la base de datos.  
        Args:  
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'images'.
        """
        db_table = 'images'