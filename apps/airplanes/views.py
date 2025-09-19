from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Airplane, AirplaneType
from .serializers import AirplaneSerializer, AirplaneTypeSerializer

class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related('airplane_type').all()
    serializer_class = AirplaneSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'airplane_type__name']
    filterset_fields = ['airplane_type']
    ordering_fields = ['name']
    ordering = ['name']