from django.db import models
from django.contrib.auth.models import User
from core.models.Category import Category 
class Recipe(models.Model):

    """
    Modelo de la tabla recipes

    Args:  
        models (Model): Clase base de Django para modelos. 

    Attributes:  
        `name (str)`: Nombre de la receta  
        `description (str)`: Descripción de la receta  
        `user_id (int)`: ID del usuario asociado a la receta, relacionado con el modelo User  
        `category_id (int)`: ID de la categoría asociada a la receta, relacionada con el modelo Category  
        `duration_minutes (int)`: Duración de la receta  
        `commensals (int)`: Comensales de la receta  
        `created_at (DateTimeField)`: Fecha y hora de creación del registro, se establece automáticamente al modificar el objeto
        `updated_at (DateTimeField)`: Fecha y hora de la última actualización del registro, se actualiza automáticamente al modificar el objeto
    
    Author:  
        {Lorena Martínez}
    """
    
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    duration_minutes = models.IntegerField()
    commensals = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:

        """
        Meta clase para definir metadatos del modelo Recipe.
        Esta clase define el nombre de la tabla en la base de datos.  
        Args:  
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'recipes'.
        """
        
        db_table = 'recipes'

    





