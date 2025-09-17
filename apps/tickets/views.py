from rest_framework import viewsets

from .models import Ticket
from .serializers import TicketSerializer, TicketListSerializer, TicketDetailSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        if self.action == 'retrieve':
            return TicketDetailSerializer
        return TicketSerializer
