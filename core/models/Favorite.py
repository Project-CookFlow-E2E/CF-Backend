from django.db import models
from django.contrib.auth.models import User
# from .models import Recipe
from django.conf import settings

class Favorite(models.Model):
    """Modelo de Favorite, representa las recetas que el usuario guarda en favoritos.  

    Args:  
        models (Model): Clase base de Django para modelos.  
    Attributes:  
        `user_id(ForeingKey)`: Relacion con el modelo User, que define el usuario.  
        `created_at (DateTimeField)`: Fecha y hora de creación del registro, se establece automáticamente al crear el objeto.  
        `updated_at (DateTimeField)`: Fecha y hora de la última actualización del registro,\n  
        se actualiza automáticamente al modificar el objeto.    
    Author:  
    {Ana Castro}
    """

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'favorites'

    """
        Meta clase para definir metadatos del modelo Favorite.
        Esta clase define el nombre de la tabla en la base de datos.  
        Args:  
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'favorites'.  
        """