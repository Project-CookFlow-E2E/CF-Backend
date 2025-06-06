import os
import uuid
from PIL import Image as PILImage
from django.conf import settings
from django.forms import ValidationError
from rest_framework import viewsets,mixins,status
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from media.models.image import Image
from media.serializers.image_serializer import (
    ImageListSerializer,
    ImageAdminSerializer,
    ImageWriteSerializer
)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

def filter_and_order_images(queryset, params):
    image_type = params.get('type')
    external_id = params.get('external_id')
    orderby = params.get('orderby', 'id')
    orderway = params.get('orderway', 'asc')

    if image_type:
        queryset = queryset.filter(type=image_type)
    if external_id:
        queryset = queryset.filter(external_id=external_id)

    allowed_order_fields = {'id', 'created_at', 'name', 'type', 'processing_status'}
    if orderby not in allowed_order_fields:
        orderby = 'id'
    if orderway == 'desc':
        orderby = f'-{orderby}'

    return queryset.order_by(orderby)

class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista de solo lectura accesible para cualquier usuario.
    Permite filtrar por type y external_id, y ordenar por campos permitidos.
    """
    queryset = Image.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return ImageListSerializer

    def get_queryset(self):
        return filter_and_order_images(super().get_queryset(), self.request.query_params)


class ImageAdminViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista de administración solo get
    """
    queryset = Image.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ImageAdminSerializer

    def get_queryset(self):
        return filter_and_order_images(super().get_queryset(), self.request.query_params)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def validate_extension(filename):
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Formato de imagen no permitido: .{ext}")

def delete_old_image_file(user_id, external_id, image_type):
    """
    Elimina archivos y registros previos asociados al mismo external_id y type.
    """
    old_images = Image.objects.filter(external_id=external_id, type=image_type)
    for img in old_images:
        if img.url:
            old_path = os.path.join(settings.MEDIA_IMG_PATH, str(user_id), img.url)
            if os.path.exists(old_path):
                os.remove(old_path)
    old_images.delete()

def save_image_to_webp(image_file, user_id):
    """
    Convierte la imagen a WEBP y la guarda en media/{user_id}/uuid.webp
    """
    validate_extension(image_file.name)
    
    user_folder = os.path.join(settings.MEDIA_IMG_PATH, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    new_filename = f"{uuid.uuid4()}.webp"
    new_path = os.path.join(user_folder, new_filename)

    image = PILImage.open(image_file)
    image.save(new_path, format="WEBP")
    return new_filename

class ImageWriteDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ImageWriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.all()

    def get_object(self):
        external_id = self.kwargs.get("id")
        image_type = self.kwargs.get("type")
        try:
            return Image.objects.get(external_id=external_id, type=image_type)
        except Image.DoesNotExist:
            raise NotFound("Imagen no encontrada con ese id y type.")

    def create(self, request, *args, **kwargs):
        image_file = request.FILES.get("file")
        if not image_file:
            raise ValidationError("Debes adjuntar un archivo de imagen con el campo 'file'.")

        external_id = request.data.get("id")
        image_type = request.data.get("type")

        if not external_id or not image_type:
            raise ValidationError("Faltan campos 'id' o 'type' en la solicitud.")

        delete_old_image_file(request.user.id, external_id, image_type)
        filename = save_image_to_webp(image_file, request.user.id)

        image = Image.objects.create(
            name=filename,
            url=filename,
            external_id=external_id,
            type=image_type,
            processing_status='UPLOADED',
        )
        serializer = self.get_serializer(image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        image_file = request.FILES.get("file")
        if not image_file:
            raise ValidationError("Debes adjuntar un archivo de imagen con el campo 'file'.")

        delete_old_image_file(request.user.id, instance.external_id, instance.type)
        filename = save_image_to_webp(image_file, request.user.id)

        instance.name = filename
        instance.url = filename
        instance.processing_status = 'UPLOADED'
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = os.path.join(settings.MEDIA_IMG_PATH, str(request.user.id), instance.url)
        if os.path.exists(file_path):
            os.remove(file_path)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
