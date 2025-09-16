from django.core.exceptions import ValidationError
from django.db import models
from apps.orders.models import Order
from apps.flights.models import Flight


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.CharField(max_length=10)
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

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["flight", "row", "seat"]
        unique_together = ["flight", "row", "seat"]

    def clean(self):
        if self.flight and self.flight.airplane:
            if self.row > self.flight.airplane.rows:
                raise ValidationError(f"Row {self.row} does not exist on this airplane")

    def __str__(self):
        return f"Ticket {self.flight} - Row {self.row}, Seat {self.seat}"