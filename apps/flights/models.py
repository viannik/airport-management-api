from django.core.exceptions import ValidationError
from django.db import models
from apps.airports.models import Airport
from apps.airplanes.models import Airplane
from apps.crews.models import Crew


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departing_routes",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arriving_routes",
    )
    distance = models.PositiveIntegerField(help_text="Distance in kilometers")

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"
        ordering = ["source", "destination"]
        unique_together = ["source", "destination"]

    def clean(self):
        if self.source == self.destination:
            raise ValidationError("Source and destination airports cannot be the same")

    def __str__(self):
        return f"{self.source} -> {self.destination}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        Crew,
        related_name="flights",
        blank=True,
    )

    class Meta:
        verbose_name = "Flight"
        verbose_name_plural = "Flights"
        ordering = ["departure_time"]

    def clean(self):
        if self.departure_time and self.arrival_time:
            if self.arrival_time <= self.departure_time:
                raise ValidationError("Arrival time must be after departure time")

    def __str__(self):
        return f"{self.route} ({self.departure_time} - {self.arrival_time})"