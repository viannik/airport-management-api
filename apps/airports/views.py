from rest_framework import filters, viewsets

from .models import Airport
from .serializers import AirportSerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'closest_big_city']
    ordering_fields = ['name', 'closest_big_city']
    ordering = ['name']