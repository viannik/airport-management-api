from django.db.models import F, Count
from rest_framework import viewsets

from .models import Flight, Route
from .serializers import (
    RouteSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    FlightCreateSerializer,
)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related("airplane").annotate(
                seats_available=(
                    F("airplane__rows") * F("airplane__seats_in_row")
                    - Count("tickets")
                )
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        if self.action == "create":
            return FlightCreateSerializer

        return FlightSerializer
