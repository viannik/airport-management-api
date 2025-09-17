from django.db import transaction
from rest_framework import serializers

from .models import Order
from apps.tickets.models import Ticket
from apps.tickets.serializers import TicketSerializer, TicketListSerializer


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
        return order

class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
