from django.db.models import F, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import FlightFilter
from .models import Flight, Route
from .serializers import (
    RouteSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    FlightCreateSerializer,
)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related('source', 'destination').all()
    serializer_class = RouteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['source__name', 'destination__name']
    ordering_fields = ['source__name', 'destination__name', 'distance']
    ordering = ['source__name', 'destination__name']


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "airplane", 
        "airplane__airplane_type",
        "route", 
        "route__source", 
        "route__destination"
    ).prefetch_related("crew").all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FlightFilter
    search_fields = ['airplane__name', 'airplane__airplane_type__name', 'route__source__name', 'route__destination__name']
    ordering_fields = ['departure_time', 'arrival_time']
    ordering = ['departure_time']

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.annotate(
                seats_available=(
                    F("airplane__rows") * F("airplane__seats_in_row")
                    - Count("tickets")
                )
            )
        elif self.action == "retrieve":
            queryset = queryset.prefetch_related("tickets")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        if self.action == "create":
            return FlightCreateSerializer

        return FlightSerializer
