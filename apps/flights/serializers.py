from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import Route, Flight
from apps.airplanes.serializers import AirplaneSerializer


class RouteSerializer(serializers.ModelSerializer):
    source = StringRelatedField(read_only=True)
    destination = StringRelatedField(read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class FlightSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)
    crew = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class FlightListSerializer(FlightSerializer):
    route = StringRelatedField(read_only=True)
    airplane = StringRelatedField(read_only=True)
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
    taken_seats = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="place", source="tickets",
    )

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


class FlightCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("route", "airplane", "departure_time", "arrival_time", "crew")