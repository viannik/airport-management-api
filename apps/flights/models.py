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

    distance = models.PositiveIntegerField()

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
    )

    def __str__(self):
        return f"{self.route} ({self.departure_time} - {self.arrival_time})"