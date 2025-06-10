from rest_framework import serializers
from recipes.models.ingredient import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    
        """
        Clase Meta del serializer IngredientSerializer.  

        Define cómo se deben representar y manejar los campos del modelo Ingredient  

        Atributos:  
        ----------
        model (Model):  
            Modelo al que hace referencia este serializer. En este caso, `Ingredient`.  

        fields (list):  
            Lista explícita de campos del modelo que serán incluidos en la serialización  
            y deserialización.   
            Incluye:  
                - id (int): Identificador único del ingrediente.  
                - name (str): Nombre del ingrediente.  
                - description (str): Descripción opcional del ingrediente.  
                - quantity (int): Cantidad del ingrediente (por ejemplo, 2).  
                - unit (str): Unidad de medida (por ejemplo, 'gramos', 'tazas').  
                - is_checked (bool): Estado que indica si el ingrediente ha sido marcado (por ejemplo, en una lista de la compra).  

        read_only_fields (list):  
            Define los campos que no pueden ser modificados por el usuario a través de peticiones POST/PUT.  
            En este caso:  
                - id: Este campo es generado automáticamente por la base de datos y no se debe modificar manualmente.  

        Uso:  
        ----
        Esta configuración asegura una serialización clara y controlada del modelo Ingredient,  
        especialmente útil para la visualización y manipulación de ingredientes en listas de recetas o compras. 

        Author:
        Noemi Casaprima    
        """
        
        class Meta:
            model = Ingredient
            fields = [
                'id',
                'name',
                'description',
                'quantity',
                'unit',
                'is_checked',
            
            ]
            read_only_fields = ['id']


class IngredientAdminSerializer(serializers.ModelSerializer):
     
        """  
        Define la configuración del modelo Ingredient para su uso con usuarios administradores,   
        permitiendo mayor nivel de acceso y edición que en el serializer estándar.  

        Atributos:  
        ----------
        model (Model):  
            Modelo al que hace referencia este serializer. En este caso, `Ingredient`.    

        fields (list):  
            Lista explícita de todos los campos disponibles del modelo Ingredient.  
            Incluye:  
                - id (int): Identificador único del ingrediente.  
                - name (str): Nombre del ingrediente.  
                - description (str): Descripción opcional del ingrediente.  
                - quantity (int): Cantidad del ingrediente.  
                - unit (str): Unidad de medida.  
                - is_checked (bool): Estado del ingrediente.  
                - created_at (datetime): Fecha de creación del ingrediente (generada automáticamente).  
                - updated_at (datetime): Fecha de última modificación del ingrediente.  

        read_only_fields (list):  
            Lista de campos protegidos contra escritura.   
            En este caso:  
                - id: Generado automáticamente, no debe ser modificado.  
                - created_at: Timestamp creado por Django.  
                - updated_at: También gestionado por el sistema internamente.  

        Uso:  
        ----
        Este serializer está diseñado específicamente para su uso en el panel de administración o   
        endpoints protegidos, donde los administradores necesitan acceso completo a los datos de los ingredientes,  
        incluyendo campos gestionados automáticamente por el sistema.  

     Author:  
        Noemi Casaprima      
        """  

        class Meta:
                model = Ingredient
                fields = '__all__'
                read_only_fields = ['id', 'created_at', 'updated_at'] 
    