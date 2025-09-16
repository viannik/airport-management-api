from django.core.validators import MaxValueValidator
from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = "Airplane Type"
        verbose_name_plural = "Airplane Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=128, unique=True)
    rows = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    seats_in_row = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes",
    )

    class Meta:
        verbose_name = "Airplane"
        verbose_name_plural = "Airplanes"
        ordering = ["name"]

    @property
    def total_seats(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} ({self.airplane_type})"