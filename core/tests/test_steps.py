# core/tests/test_models.py

import pytest
from core.models.Step import Step
from core.models.Recipe import Recipe


@pytest.mark.django_db
def test_create_step_basico():
    """
    Verifica que un objeto Step se cree correctamente sin relación a Recipe.
    """
    step = Step.objects.create(
        order=1,
        description='Precalentar el horno'
    )

    assert step.order == 1
    assert step.description == 'Precalentar el horno'
    assert step.created_at is not None
    assert step.updated_at is not None
    assert step.created_at <= step.updated_at


# Si habilitas la ForeignKey a Recipe, descomenta este test:
#
@pytest.mark.django_db
def test_create_step_con_recipe():
    """
    Verifica que un objeto Step se cree correctamente cuando está relacionado
    con un objeto Recipe.
    """
    # Primero creamos una receta de ejemplo
    recipe = Recipe.objects.create(name='Tarta de manzana')

    # Ahora creamos el Step apuntando a esa receta
    step = Step.objects.create(
        order=1,
        description='Pelar las manzanas',
        recipe=recipe
    )

    assert step.order == 1
    assert step.description == 'Pelar las manzanas'
    assert step.recipe == recipe
    assert step.created_at is not None
    assert step.updated_at is not None
    assert step.created_at <= step.updated_at
