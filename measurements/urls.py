""" Módulo para definir las URLs de la aplicación de mediciones.
Este módulo utiliza el enrutador predeterminado de Django REST Framework
para registrar los conjuntos de vistas de unidades y tipos de unidades.

Author:
    {Angel Aragón}
"""
from rest_framework.routers import DefaultRouter
from measurements.views.measurementView import UnitViewSet, UnitTypeViewSet

router = DefaultRouter()
router.register(r'units', UnitViewSet)
router.register(r'unit-types', UnitTypeViewSet)

urlpatterns = router.urls