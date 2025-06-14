from django.conf import settings
from django.db import models
from recipes.models.category import Category 
from measurements.models.unitType import UnitType

class Ingredient(models.Model):
    """ Model representa un modelo en el sistema de ingredientes.
    Esta clase hereda de Django's Model y define la estructura de la tabla de ingredientes en la base de datos.,    
     Arguments:  
       models (Model): Clase base para Django para modelos.  
     Atributes:    
        `name (str)`: Nombre del ingrediente maximo de letras 50 y tiene que ser unico.  
        `user_id (User)`: Usuario que creo el ingrediente
        `unit_type_id`:Tipo de unidad.    
        `is_approved (bool)`; indica que el ingrediente esta aprobado.  
        `created_at (datetime)`: Fecha y hora  en el que fue creado el ingrediente.  
        `updated_at (datetime)`: Fecha y hora  en el que es actualizado el ingredientes.  
        
       Authors:
        - [Noemi Casaprima] """

    name = models.CharField(max_length=50, unique=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit_type_id = models.ForeignKey(UnitType, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(
      Category,
      related_name='ingredients',
      db_table='categories_ingredients' 
    )

    class Meta:
        """ Meta class Define el nombre de la tabla.
        arguments:
        - db_table (str): Es el nombre de la tabla en este caso.
        """
        db_table = 'ingredients'

    def __str__(self):
        return self.name
        
        

