import pytest
from core.models.Image import Image
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestImageModel:

    def test_create_image_minimal(self):
        image = Image.objects.create(
            name="hash_123",
            type=Image.ImageType.RECIPE,
            url="https://example.com/image.jpg",
            processing_status=Image.ImageStatus.UPLOADED,
            external_id=1
        )
        assert image.id is not None
        assert image.name == "hash_123"
        assert image.type == Image.ImageType.RECIPE
        assert image.processing_status == Image.ImageStatus.UPLOADED

    def test_invalid_type_choice_raises_error(self):
        with pytest.raises(ValidationError):
            image = Image(
                name="hash_124",
                type="INVALID",
                url="https://example.com/image2.jpg",
                processing_status=Image.ImageStatus.UPLOADED,
                external_id=2
            )
            image.full_clean()  

    def test_invalid_status_choice_raises_error(self):
        with pytest.raises(ValidationError):
            image = Image(
                name="hash_125",
                type=Image.ImageType.STEP,
                url="https://example.com/image3.jpg",
                processing_status="INVALID",
                external_id=3
            )
            image.full_clean()

    def test_missing_required_field_raises_integrity_error(self):
        with pytest.raises(IntegrityError):
            Image.objects.create(
                name="hash_126",
                type=Image.ImageType.USER,
                url="https://example.com/image4.jpg"
            )

    def test_choices_are_enforced_on_save(self):
        image = Image(
            name="hash_127",
            type=Image.ImageType.USER,
            url="https://example.com/image5.jpg",
            processing_status="PROCESSING",
            external_id=10
        )
        image.full_clean()
        image.save()
        assert image.processing_status == Image.ImageStatus.PROCESSING