from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType
from measurements.serializers.unitSerializer import UnitSerializer, UnitAdminSerializer
from measurements.serializers.unitTypeSerializer import UnitTypeSerializer, UnitTypeAdminSerializer
from django_filters.rest_framework import DjangoFilterBackend

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['unit_type', 'id']

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS and self.request.user and self.request.user.is_staff:
            return UnitAdminSerializer
        return UnitSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]

class UnitTypeViewSet(viewsets.ModelViewSet):
    queryset = UnitType.objects.all()

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS and self.request.user and self.request.user.is_staff:
            return UnitTypeAdminSerializer
        return UnitTypeSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]