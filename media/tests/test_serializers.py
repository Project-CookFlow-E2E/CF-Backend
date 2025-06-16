import pytest
from rest_framework.exceptions import ValidationError
from model_bakery import baker
from django.utils import timezone
from django.db import IntegrityError

from media.models.image import Image
from media.serializers.image_serializer import (
    ImageAdminSerializer,
    ImageWriteSerializer,
    ImageListSerializer
)

@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.media_app
class TestImageSerializers:
    """
    Tests for Image serializers in the media app.
    Covers Admin, Write, and List serializers.
    """

    @pytest.fixture
    def setup_image_data(self):
        """
        Fixture to set up a sample Image instance for serialization tests.
        """
        image_instance = baker.make(
            Image,
            name='test_hash_xyz',
            url='http://example.com/test_xyz.jpg',
            type=Image.ImageType.RECIPE,
            processing_status=Image.ImageStatus.COMPLETED,
            external_id=12345,
            created_at=timezone.now()
        )
        return {'image': image_instance}

    # --- ImageAdminSerializer Tests ---
    def test_image_admin_serializer_serialization(self, setup_image_data):
        """
        Tests ImageAdminSerializer for correct serialization of all fields, including display values.
        Ensures all fields are read-only.
        """
        image = setup_image_data['image']
        serializer = ImageAdminSerializer(instance=image)
        data = serializer.data

        assert data['id'] == image.id
        assert data['name'] == image.name
        assert data['url'] == image.url
        assert data['type'] == image.type
        assert data['type_display'] == image.get_type_display()
        assert data['processing_status'] == image.processing_status
        assert data['processing_status_display'] == image.get_processing_status_display()
        assert data['external_id'] == image.external_id
        assert 'created_at' in data

        for field_name, field_obj in serializer.fields.items():
            assert field_obj.read_only, f"Field '{field_name}' should be read-only"

    def test_image_admin_serializer_no_creation(self):
        """
        Tests that ImageAdminSerializer cannot be used for creation (as all fields are read-only).
        """
        data = {
            'name': 'new_img',
            'url': 'http://new.com/img.jpg',
            'type': Image.ImageType.USER,
            'processing_status': Image.ImageStatus.UPLOADED,
            'external_id': 1
        }
        serializer = ImageAdminSerializer(data=data)
        assert serializer.is_valid()
        with pytest.raises(IntegrityError, match="null value in column \"external_id\""):
            serializer.save()

    def test_image_admin_serializer_no_update(self, setup_image_data):
        """
        Tests that ImageAdminSerializer cannot be used for updates (as all fields are read-only).
        """
        image = setup_image_data['image']
        update_data = {'name': 'updated_name', 'url': 'http://updated.com/img.jpg'}
        serializer = ImageAdminSerializer(instance=image, data=update_data, partial=True)
        assert serializer.is_valid()

        updated_instance = serializer.save()
        assert updated_instance.name == image.name
        assert updated_instance.url == image.url
        assert updated_instance.processing_status == image.processing_status


    # --- ImageWriteSerializer Tests ---
    def test_image_write_serializer_create_valid(self):
        """
        Tests ImageWriteSerializer can create a new Image instance with valid data.
        """
        data = {
            'name': 'new_image_hash',
            'url': 'http://new.example.com/new.jpg',
            'type': Image.ImageType.RECIPE,
            'processing_status': Image.ImageStatus.UPLOADED,
            'external_id': 100
        }
        serializer = ImageWriteSerializer(data=data)
        assert serializer.is_valid(raise_exception=True)
        image = serializer.save()

        assert image.id is not None
        assert image.name == 'new_image_hash'
        assert image.url == 'http://new.example.com/new.jpg'
        assert image.type == Image.ImageType.RECIPE
        assert image.processing_status == Image.ImageStatus.UPLOADED
        assert image.external_id == 100
        assert image.created_at is not None

    def test_image_write_serializer_update_valid(self, setup_image_data):
        """
        Tests ImageWriteSerializer can update an existing Image instance.
        """
        image = setup_image_data['image']
        update_data = {
            'name': 'updated_hash',
            'url': 'http://updated.example.com/updated.jpg',
            'processing_status': Image.ImageStatus.COMPLETED
        }
        serializer = ImageWriteSerializer(instance=image, data=update_data, partial=True)
        assert serializer.is_valid(raise_exception=True)
        updated_image = serializer.save()

        assert updated_image.name == 'updated_hash'
        assert updated_image.url == 'http://updated.example.com/updated.jpg'
        assert updated_image.processing_status == Image.ImageStatus.COMPLETED
        assert updated_image.id == image.id
        assert updated_image.type == image.type
        assert updated_image.external_id == image.external_id


    def test_image_write_serializer_invalid_type(self):
        """
        Tests ImageWriteSerializer validation for an invalid 'type' choice.
        """
        data = {
            'name': 'bad_type_img',
            'url': 'http://bad.com/img.jpg',
            'type': 'INVALID_TYPE',
            'processing_status': Image.ImageStatus.UPLOADED,
            'external_id': 1
        }
        serializer = ImageWriteSerializer(data=data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert 'type' in excinfo.value.detail
        assert "is not a valid choice" in excinfo.value.detail['type'][0]

    def test_image_write_serializer_invalid_processing_status(self):
        """
        Tests ImageWriteSerializer validation for an invalid 'processing_status' choice.
        """
        data = {
            'name': 'bad_status_img',
            'url': 'http://bad.com/img.jpg',
            'type': Image.ImageType.USER,
            'processing_status': 'UNKNOWN_STATUS',
            'external_id': 1
        }
        serializer = ImageWriteSerializer(data=data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert 'processing_status' in excinfo.value.detail
        assert "is not a valid choice" in excinfo.value.detail['processing_status'][0]

    def test_image_write_serializer_missing_required_fields(self):
        """
        Tests ImageWriteSerializer validation for missing required fields during creation.
        """
        data = {
            'url': 'http://missing.com/img.jpg',
            'processing_status': Image.ImageStatus.UPLOADED,
        }
        serializer = ImageWriteSerializer(data=data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert 'name' in excinfo.value.detail
        assert 'type' in excinfo.value.detail
        assert 'external_id' in excinfo.value.detail
        assert 'This field is required.' in excinfo.value.detail['name']


    # --- ImageListSerializer Tests ---
    def test_image_list_serializer_serialization(self, setup_image_data):
        """
        Tests ImageListSerializer for correct serialization of limited fields.
        Ensures all fields are read-only.
        """
        image = setup_image_data['image']
        serializer = ImageListSerializer(instance=image)
        data = serializer.data

        assert data['id'] == image.id
        assert data['url'] == image.url
        assert data['type'] == image.type
        assert data['external_id'] == image.external_id
        assert data['processing_status'] == image.processing_status
        assert len(data) == 5
        assert 'name' not in data
        assert 'created_at' not in data

        for field_name, field_obj in serializer.fields.items():
            assert field_obj.read_only, f"Field '{field_name}' should be read-only"

    def test_image_list_serializer_no_creation(self):
        """
        Tests that ImageListSerializer cannot be used for creation, leading to IntegrityError.
        """
        data = {
            'url': 'http://list.com/img.jpg',
            'type': Image.ImageType.USER,
            'external_id': 500,
            'name': 'temp_name_for_creation_attempt',
            'processing_status': Image.ImageStatus.UPLOADED
        }
        serializer = ImageListSerializer(data=data)
        assert serializer.is_valid()

        with pytest.raises(IntegrityError):
            serializer.save()

    def test_image_list_serializer_no_update(self):
        """
        Tests that ImageListSerializer cannot be used for updates.
        """
        image = baker.make(Image, url='original.jpg', type=Image.ImageType.USER, external_id=1, name='orig')
        serializer_update = ImageListSerializer(instance=image, data={'url': 'new.jpg'}, partial=True)
        assert serializer_update.is_valid()
        updated_image = serializer_update.save()
        assert updated_image.url == image.url
