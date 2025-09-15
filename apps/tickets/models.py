from django.db import models
from apps.orders.models import Order
from apps.flights.models import Flight


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.CharField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )