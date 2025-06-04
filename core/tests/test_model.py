import pytest
from core.models import Unit
from django.utils import timezone

@pytest.mark.django_db
def test_create_unit():
    unidad = Unit.objects.create(name="gramo")

    assert unidad.id is not None
    assert unidad.name == "gramo"
    assert isinstance(unidad.created_at, timezone.datetime)
