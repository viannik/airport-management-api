from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import Route, Flight
from apps.airplanes.serializers import AirplaneSerializer
from apps.crews.serializers import CrewSerializer
from apps.tickets.serializers import TicketSeatsSerializer


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class FlightSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class FlightListSerializer(FlightSerializer):
    route = StringRelatedField(read_only=True)
    airplane = StringRelatedField(read_only=True)
    crew = StringRelatedField(many=True, read_only=True)
    seats_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "seats_available",
        )


class FlightDetailSerializer(FlightSerializer):
    taken_seats = TicketSeatsSerializer(many=True, read_only=True, source="tickets")

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "taken_seats",
        )