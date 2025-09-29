from rest_framework import filters, viewsets

from .models import Ticket
from .serializers import TicketSerializer, TicketListSerializer, TicketDetailSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        'flight', 
        'flight__route__source', 
        'flight__route__destination',
        'flight__airplane__airplane_type',
        'order',
        'order__user'
    ).all()
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['seat', 'flight__route__source__name', 'flight__route__destination__name']
    ordering_fields = ['row', 'seat', 'flight__departure_time']
    ordering = ['flight', 'row', 'seat']

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        if self.action == 'retrieve':
            return TicketDetailSerializer
        return TicketSerializer
