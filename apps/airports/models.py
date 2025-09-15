from django.db import models

class Airport(models.Model):
    name = models.CharField(max_length=128)
    closest_big_city = models.CharField(max_length=128)

    def __str__(self):
        return self.name