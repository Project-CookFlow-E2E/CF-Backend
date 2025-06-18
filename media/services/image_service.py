import os
import uuid
from django.conf import settings
from PIL import Image as PILImage
from media.models import Image
from django.forms import ValidationError

import logging

# Configura el logger para la aplicación, asumiendo que ya hay una configuración global en settings.py
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def validate_extension(filename):
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        logger.error(f"ValidationError: Formato de imagen no permitido: .{ext} para archivo {filename}")
        raise ValidationError(f"Formato de imagen no permitido: .{ext}")


def remove_image_file(user_id, filename):
    if not filename:
        logger.warning("No se proporcionó nombre de archivo para remove_image_file, omitiendo.")
        return
    # Asumiendo que 'filename' es solo el nombre único del archivo, y la ruta se construye
    # con 'MEDIA_IMG_PATH / user_id / filename'
    path = os.path.join(settings.MEDIA_IMG_PATH, str(user_id), filename)
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError as e:
            logger.error(f"Error al eliminar archivo {path}: {e}", exc_info=True)


def save_file_to_disk(image_file, user_id):
    try:
        folder = os.path.join(settings.MEDIA_IMG_PATH, str(user_id))
        os.makedirs(folder, exist_ok=True)

        new_filename = f"{uuid.uuid4()}.webp"
        full_path = os.path.join(folder, new_filename)

        image = PILImage.open(image_file)
        # Convierte a RGB si no lo está, ya que WebP típicamente no soporta RGBA para guardar
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(full_path, format="WEBP")
        return new_filename
    except Exception as e:
        logger.error(f"Error en save_file_to_disk para {image_file.name}: {e}", exc_info=True)
        raise # Vuelve a lanzar la excepción para que sea capturada por el try-except principal


def update_image_for_instance(image_file, user_id, external_id, image_type):
    """
    Actualiza el archivo de una imagen ya existente. Si no existe, la crea.
    """
    if not image_file:
        logger.warning("No se proporcionó image_file a update_image_for_instance. Retornando None.")
        return None

    try:
        validate_extension(image_file.name)
        new_filename = save_file_to_disk(image_file, user_id)

        try:
            image_obj = Image.objects.get(external_id=external_id, type=image_type)
            # Borra archivo anterior
            remove_image_file(user_id, image_obj.url)
            # Actualiza campos
            image_obj.name = new_filename
            image_obj.url = new_filename # URL debería ser la ruta relativa/nombre de archivo
            image_obj.processing_status = Image.ImageStatus.COMPLETED # Usar la constante
            image_obj.save()
            return image_obj
        except Image.DoesNotExist:
            new_image_obj = Image.objects.create(
                name=new_filename,
                url=new_filename, # URL debería ser la ruta relativa/nombre de archivo
                external_id=external_id,
                type=image_type,
                processing_status=Image.ImageStatus.COMPLETED # Usar la constante
            )
            return new_image_obj

    except ValidationError as e:
        logger.error(f"Error de validación en update_image_for_instance: {e}", exc_info=True)
        raise # Vuelve a lanzar para asegurar que se propague a DRF
    except Exception as e:
        logger.error(f"Error general en update_image_for_instance para archivo {image_file.name}: {e}", exc_info=True)
        return None