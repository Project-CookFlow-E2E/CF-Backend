import pytest
from model_bakery import baker
from media.models.image import Image

@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.media_app
class TestImageModel:
    """
    Tests for the Image model in the media app.
    Ensures model fields, choices, and __str__ method work as expected.
    """

    def test_image_creation(self):
        """
        Tests that an Image instance can be created successfully with valid data.
        """
        image = baker.make(
            Image,
            name='test_image_hash_123',
            url='http://example.com/test_image.jpg',
            type=Image.ImageType.RECIPE,
            processing_status=Image.ImageStatus.COMPLETED,
            external_id=123
        )

        assert image.id is not None
        assert image.name == 'test_image_hash_123'
        assert image.url == 'http://example.com/test_image.jpg'
        assert image.type == Image.ImageType.RECIPE
        assert image.processing_status == Image.ImageStatus.COMPLETED
        assert image.external_id == 123
        assert image.created_at is not None

    def test_image_default_processing_status(self):
        """
        Tests that the default processing_status is set correctly upon creation.
        """
        image = baker.make(
            Image,
            name='default_status_img',
            url='http://example.com/default.jpg',
            type=Image.ImageType.USER,
            external_id=1
        )
        assert image.processing_status == 'uploaded' # Ensure it matches your model's default string

    def test_image_str_representation(self):
        """
        Tests the string representation of the Image model.
        """
        image = baker.make(
            Image,
            name='my_pic',
            url='http://example.com/mypic.png',
            type=Image.ImageType.STEP,
            external_id=456
        )
        # Assuming the __str__ method will return the name or a combination
        # If no __str__ is defined, it defaults to 'Image object (ID)'
        assert str(image) == f"Image object ({image.id})" # Default if no __str__ defined
        # If you add a __str__ method, update this assertion. Example:
        # assert str(image) == f"{image.name} ({image.type})"

    def test_image_type_choices(self):
        """
        Tests that ImageType choices are valid and correctly stored.
        """
        image_user = baker.make(Image, type=Image.ImageType.USER, external_id=1, name='u1', url='a.com/u1')
        image_recipe = baker.make(Image, type=Image.ImageType.RECIPE, external_id=2, name='r1', url='a.com/r1')
        image_step = baker.make(Image, type=Image.ImageType.STEP, external_id=3, name='s1', url='a.com/s1')

        assert image_user.type == 'USER'
        assert image_recipe.type == 'RECIPE'
        assert image_step.type == 'STEP'

        assert image_user.get_type_display() == 'User'
        assert image_recipe.get_type_display() == 'Recipe'
        assert image_step.get_type_display() == 'Step'

    def test_image_status_choices(self):
        """
        Tests that ImageStatus choices are valid and correctly stored.
        """
        image_uploaded = baker.make(Image, processing_status=Image.ImageStatus.UPLOADED, external_id=1, name='upd', url='a.com/upd')
        image_processing = baker.make(Image, processing_status=Image.ImageStatus.PROCESSING, external_id=2, name='prc', url='a.com/prc')
        image_completed = baker.make(Image, processing_status=Image.ImageStatus.COMPLETED, external_id=3, name='cmp', url='a.com/cmp')
        image_failed = baker.make(Image, processing_status=Image.ImageStatus.FAILED, external_id=4, name='fld', url='a.com/fld')

        assert image_uploaded.processing_status == 'UPLOADED'
        assert image_processing.processing_status == 'PROCESSING'
        assert image_completed.processing_status == 'COMPLETED'
        assert image_failed.processing_status == 'FAILED'

        assert image_uploaded.get_processing_status_display() == 'Uploaded'
        assert image_processing.get_processing_status_display() == 'Processing'
        assert image_completed.get_processing_status_display() == 'Completed'
        assert image_failed.get_processing_status_display() == 'Failed'

    def test_image_name_max_length(self):
        """
        Tests that the 'name' field respects its max_length constraint.
        """
        long_name = 'a' * 101 # Longer than 100
        with pytest.raises(Exception): # Catching a general exception as Django might raise ValidationError or TruncationError
            baker.make(Image, name=long_name, url='http://example.com/short.jpg', type=Image.ImageType.USER, external_id=1)

    def test_image_url_max_length(self):
        """
        Tests that the 'url' field respects its max_length constraint.
        """
        long_url = 'http://example.com/' + 'a' * 80 + '.jpg' # Longer than 100
        with pytest.raises(Exception): # Catching a general exception as Django might raise ValidationError or TruncationError
            baker.make(Image, url=long_url, name='short_name', type=Image.ImageType.USER, external_id=1)

