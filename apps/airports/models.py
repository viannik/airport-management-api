from django.db import models

class Airport(models.Model):
    name = models.CharField(max_length=128, unique=True)
    closest_big_city = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Airport"
        verbose_name_plural = "Airports"
        ordering = ["name"]

    def __str__(self):
        return self.name