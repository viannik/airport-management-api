from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.airports.models import Airport
from apps.airplanes.models import Airplane, AirplaneType
from apps.crews.models import Crew
from .models import Flight, Route
from apps.orders.models import Order
from apps.tickets.models import Ticket


def setup_flight_data(self):
    self.airport1 = Airport.objects.create(name="Kyiv Airport", closest_big_city="Kyiv")
    self.airport2 = Airport.objects.create(name="Lviv Airport", closest_big_city="Lviv")
    self.airport3 = Airport.objects.create(name="Odesa Airport", closest_big_city="Odesa")

    self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
    self.airplane1 = Airplane.objects.create(name="UA-001", rows=30, seats_in_row=6, airplane_type=self.airplane_type)
    self.airplane2 = Airplane.objects.create(name="UA-002", rows=25, seats_in_row=4, airplane_type=self.airplane_type)

    self.crew1 = Crew.objects.create(first_name="John", last_name="Doe")
    self.crew2 = Crew.objects.create(first_name="Jane", last_name="Smith")

    self.route1 = Route.objects.create(source=self.airport1, destination=self.airport2, distance=500)
    self.route2 = Route.objects.create(source=self.airport2, destination=self.airport3, distance=300)

    self.flight = Flight.objects.create(
        route=self.route1,
        airplane=self.airplane1,
        departure_time=datetime.now() + timedelta(hours=2),
        arrival_time=datetime.now() + timedelta(hours=4)
    )
    self.flight.crew.add(self.crew1)
    self.flight.crew.add(self.crew2)

    self.list_url = reverse('flight-list')
    self.detail_url = reverse('flight-detail', kwargs={'pk': self.flight.pk})
    
    


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        setup_flight_data(self)

    def test_flight_list_unauthorized(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_create_unauthorized(self):
        data = {'route': self.route1.pk, 'airplane': self.airplane1.pk, 'departure_time': datetime.now(), 'arrival_time': datetime.now()}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(self.user)
        setup_flight_data(self)

    def test_can_list_flights(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_cannot_create_flight(self):
        data = {'route': self.route1.pk, 'airplane': self.airplane1.pk, 'departure_time': datetime.now(), 'arrival_time': datetime.now()}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_flight(self):
        data = {'distance': 1000}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_flight_list_serializer_seats_available(self):
        response = self.client.get(self.list_url)
        flight_data = response.data['results'][0]
        self.assertIn('seats_available', flight_data)
        self.assertEqual(flight_data['seats_available'], 180)

    def test_flight_detail_serializer_taken_seats(self):
        order = Order.objects.create(user=self.user)
        Ticket.objects.create(row=5, seat=4, flight=self.flight, order=order)

        response = self.client.get(self.detail_url)
        self.assertIn('taken_seats', response.data)
        self.assertEqual(len(response.data['taken_seats']), 1)


class AdminFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='adminpass123', is_staff=True)
        self.client.force_authenticate(self.admin_user)
        setup_flight_data(self)

    def test_admin_can_view_flights(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_admin_can_create_flight(self):
        data = {
            'route': self.route2.pk,
            'airplane': self.airplane2.pk,
            'departure_time': (datetime.now() + timedelta(hours=2)).isoformat(),
            'arrival_time': (datetime.now() + timedelta(hours=4)).isoformat()
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 2)
