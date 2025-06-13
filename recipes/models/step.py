from django.conf import settings
from django.db import models
from recipes.models.recipe import Recipe

class Step(models.Model):
    """
        Modelo de Step, representa los pasos a seguier en una receta  

    Args:
        models (Model): Clase base de Django para modelos.  
    Attributes:  
        `order  (Integer)`: columna numero de orden no puede ser nulo.  
        `recipe_id (BigInteger)`: Columna que se relaciona con otra tabla (recipes.id) mediante clave foránea.  
        `description (str)`: descripcion del paso  y tener una longitud máxima de 100 caracteres.  
        `created_at (DateTimeField)`: Fecha y hora de creación del registro, se establece automáticamente al crear el objeto. 
        `updated_at (DateTimeField)`: Fecha y hora de la última actualización del registro, se actualiza automáticamente al modificar el objeto
    Author:  
	    {Rafael Fernández}

    """
    order = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)  
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta clase para definir metadatos del modelo Unit.
            Esta clase define el nombre de la tabla en la base de datos.  
        Args:  
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'units'.
        """

        db_table = 'steps'

    def __str__(self):
        return f"Step {self.order} for {self.recipe.name}: {self.description[:30]}..."