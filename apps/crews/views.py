from rest_framework import filters, viewsets

from .models import Crew
from .serializers import CrewSerializer

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name']
    ordering = ['last_name', 'first_name']