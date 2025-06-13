import os
import uuid
from django.conf import settings
from PIL import Image as PILImage
from media.models.image import Image
from django.forms import ValidationError

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def validate_extension(filename):
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Formato de imagen no permitido: .{ext}")

def remove_image_file(user_id, filename):
    if not filename:
        return
    path = os.path.join(settings.MEDIA_IMG_PATH, str(user_id), filename)
    if os.path.exists(path):
        os.remove(path)

def save_file_to_disk(image_file, user_id):
    folder = os.path.join(settings.MEDIA_IMG_PATH, str(user_id))
    os.makedirs(folder, exist_ok=True)

    new_filename = f"{uuid.uuid4()}.webp"
    full_path = os.path.join(folder, new_filename)

    image = PILImage.open(image_file)
    image.save(full_path, format="WEBP")

    return new_filename

def update_image_for_instance(image_file, user_id, external_id, image_type):
    """
    Actualiza el archivo de una imagen ya existente. Si no existe, la crea.
    """
    validate_extension(image_file.name)
    new_filename = save_file_to_disk(image_file, user_id)

    try:
        image_obj = Image.objects.get(external_id=external_id, type=image_type)
        # Borra archivo anterior
        remove_image_file(user_id, image_obj.url)
        # Actualiza campos
        image_obj.name = new_filename
        image_obj.url = new_filename
        image_obj.processing_status = "UPLOADED"
        image_obj.save()
        return image_obj
    except Image.DoesNotExist:
        return Image.objects.create(
            name=new_filename,
            url=new_filename,
            external_id=external_id,
            type=image_type,
            processing_status="UPLOADED"
        )
