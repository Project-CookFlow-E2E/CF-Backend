from django.conf import settings
from django.db import models
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit

class ShoppingListItem(models.Model):

    """
    Modelo de la tabla shopping_list_items

    Args:  
        models (Model): Clase base de Django para modelos. 

    Attributes:  
        `user_id (int)`: ID del usuario asociado al ítem, relacionado con el modelo User  
        `ingredient_id (int)`: ID del ingrediente asociado al ítem, relacionado con el modelo Ingredient  
        `quantity_needed (int)`: Cantidad necesaria del ingrediente  
        `unit (str)`: Unidad de medida para la cantidad del ingrediente (por defecto 'pending')  
        `is_purchased (bool)`: Indica si el ingrediente ya fue comprado
        `created_at (DateTimeField)`: Fecha y hora de creación del registro  
        `updated_at (DateTimeField)`: Fecha y hora de la última actualización del registro 
        
    Author:  
        {Lorena Martínez}
    """

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_needed = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    is_purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:

        """
        Meta clase para definir metadatos del modelo Shopping_list_item.
        Esta clase define el nombre de la tabla en la base de datos.  
        Args:  
            db_table (str): Nombre de la tabla en la base de datos, en este caso 'shopping_list_items'.
        """
        
        db_table = 'shopping_list_items'

    def __str__(self):
        """
        Retorna una representación de cadena del ítem de la lista de compras.
        """
        ingredient_name = self.ingredient_id.name if self.ingredient_id else 'N/A Ingredient'
        unit_name = self.unit.name if self.unit else 'N/A Unit'
        username = self.user_id.username if self.user_id else 'N/A User'
        return f"{self.quantity_needed} {unit_name} of {ingredient_name} for {username}"
    





