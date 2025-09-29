from datetime import datetime, timedelta
from apps.users.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.tickets.models import Ticket
from apps.orders.models import Order
from apps.flights.models import Flight, Route
from apps.airports.models import Airport
from apps.airplanes.models import Airplane, AirplaneType


class TicketModelTests(TestCase):
    def setUp(self):
        self.airport1 = Airport.objects.create(
            name="Test Airport 1", closest_big_city="City 1"
        )
        self.airport2 = Airport.objects.create(
            name="Test Airport 2", closest_big_city="City 2"
        )
        self.route = Route.objects.create(
            source=self.airport1, destination=self.airport2, distance=500
        )
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="UA-001", rows=30, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=datetime.now() + timedelta(hours=2),
            arrival_time=datetime.now() + timedelta(hours=4),
        )
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpass123"
        )
        self.order = Order.objects.create(user=self.user)

    def test_ticket_place_property(self):
        ticket = Ticket.objects.create(
            row=5, seat="A", flight=self.flight, order=self.order
        )
        self.assertEqual(ticket.place, "5A")

    def test_ticket_row_validation(self):
        with self.assertRaises(ValidationError):
            ticket = Ticket(row=35, seat="A", flight=self.flight, order=self.order)
            ticket.clean()

    def test_ticket_unique_constraint(self):
        Ticket.objects.create(row=5, seat="A", flight=self.flight, order=self.order)
        with self.assertRaises(IntegrityError):
            Ticket.objects.create(row=5, seat="A", flight=self.flight, order=self.order)