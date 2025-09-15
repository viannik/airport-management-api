from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=128)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes",
    )

    def __str__(self):
        return self.name