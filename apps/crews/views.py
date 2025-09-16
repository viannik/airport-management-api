from rest_framework import viewsets

from .models import Crew
from .serializers import CrewSerializer

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer