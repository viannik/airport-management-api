from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Airplane, AirplaneType

class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")

class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = SlugRelatedField(
        slug_field="name",
        queryset=AirplaneType.objects.all(),
        required=False,
        allow_null=True,
    )
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "total_seats",
            "airplane_type",
        )