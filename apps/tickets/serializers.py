from rest_framework import serializers

from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    flight = serializers.StringRelatedField()
    order = serializers.StringRelatedField()

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")
