import django_filters
from .models import Flight


class FlightFilter(django_filters.FilterSet):
    seats_available = django_filters.NumberFilter(field_name='seats_available', lookup_expr='gte', label="Seats Available (minimum)")

    class Meta:
        model = Flight
        fields = ['airplane__airplane_type', 'seats_available']
