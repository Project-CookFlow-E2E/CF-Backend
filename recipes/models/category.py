from django.db import models
from django.conf import settings


def default_user():
    return 1

class Category(models.Model):
    """Modelo de Category, representa las diferentes categorias.  

    Args:  
        models (Model): Clase base de Django para modelos.  
    Attributes:  
        `name(str)`: Nombre de la unidad, debe ser único y tener una longitud máxima de 50 caracteres.  
        `user_id(ForeingKey)`: Relacion con el modelo User, que define el usuario.  
        `parent_category_id(ForeingKey)`: Id de la categoria padre a la que va asociada la categoria en cuestión.  
        `created_at (DateTimeField)`: Fecha y hora de creación del registro, se establece automáticamente al crear el objeto.          
        se actualiza automáticamente al modificar el objeto.    
    Author:  
    {Ana Castro}
    """
    name = models.CharField(max_length=50, unique=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=default_user)
    parent_category_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'

    """
        Meta clase para definir metadatos del modelo Category.  
        Esta clase define el nombre de la tabla en la base de datos.  
        Args:  
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'categories'.  
        """  

    def __str__(self):
        return self.name  
