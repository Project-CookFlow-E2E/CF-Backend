from rest_framework import serializers
from media.models.image import Image
""""
------------------------------------------------------------------------------
 Serializer de solo lectura para mostrar detalles completos de una imagen.
 Incluye los campos legibles (`_display`) para los campos con choices.
 Ideal para endpoints de tipo GET en frontend o admin.
------------------------------------------------------------------------------"""
class ImageAdminSerializer(serializers.ModelSerializer):
    """ Campo que devuelve el valor legible del campo `type` (por ejemplo, "User" en lugar de "USER")."""
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    """ Campo que devuelve el valor legible del campo `processing_status`."""
    processing_status_display = serializers.CharField(source='get_processing_status_display', read_only=True)

    class Meta:
        model = Image
        """ Lista completa de campos que se incluirán en la respuesta."""
        fields = [
            'id',
            'name',
            'url',
            'type',
            'type_display',
            'processing_status',
            'processing_status_display',
            'external_id',
            'created_at',
        ]
        read_only_fields = fields

""" ------------------------------------------------------------------------------
 Serializer de escritura para crear o actualizar imágenes.
 No incluye campos calculados ni automáticos.
 Ideal para formularios en paneles de administración o llamadas POST/PUT.
 ------------------------------------------------------------------------------"""
class ImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        # Solo se incluyen campos editables.
        fields = [
            'name',
            'url',
            'type',
            'processing_status',
            'external_id'
        ]

""" ------------------------------------------------------------------------------
 Serializer de lectura simplificado para vistas en lista (por ejemplo, tarjetas).
 Muestra solo los campos mínimos necesarios para representar una imagen.
 Ideal para vistas tipo "galería" o listados con rendimiento optimizado.
 ------------------------------------------------------------------------------"""
class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'url',
            'type',
            'external_id',
            'processing_status'
        ]
        read_only_fields = fields
