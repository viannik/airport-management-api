from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.airports.models import Airport
from apps.airplanes.models import Airplane, AirplaneType
from apps.flights.models import Flight, Route
from apps.users.models import User
from .models import Order

def setup_order_data(self):
    self.user1 = User.objects.create_user(email='user1@test.com', password='testpass123',)
    self.user2 = User.objects.create_user(email='user2@test.com', password='testpass123',)
    self.admin_user = User.objects.create_user(email='admin@test.com', password='adminpass123', is_staff=True,)

    airport1 = Airport.objects.create(name="Kyiv Airport", closest_big_city="Kyiv",)
    airport2 = Airport.objects.create(name="Lviv Airport", closest_big_city="Lviv",)

    airplane_type = AirplaneType.objects.create(name="Boeing 737",)
    airplane = Airplane.objects.create(name="UA-001", rows=30, seats_in_row=6, airplane_type=airplane_type,)

    route = Route.objects.create(source=airport1, destination=airport2, distance=500,)

    self.flight = Flight.objects.create(
        route=route,
        airplane=airplane,
        departure_time=datetime.now() + timedelta(hours=2),
        arrival_time=datetime.now() + timedelta(hours=4)
    )

    self.list_url = reverse("order-list")


class UnauthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        setup_order_data(self)

    def test_list_orders_unauthorized(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_unauthorized(self):
        data = {'tickets': [{'row': 1, 'seat': 'A', 'flight': self.flight.pk}]}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        setup_order_data(self)
        self.client.force_authenticate(self.user1)

    def test_can_create_order(self):
        data = {
            'tickets': [
                {'row': 1, 'seat': 'A', 'flight': self.flight.pk},
                {'row': 1, 'seat': 'B', 'flight': self.flight.pk}
            ]
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user1)
        self.assertEqual(order.tickets.count(), 2)

    def test_can_see_only_own_orders(self):
        Order.objects.create(user=self.user1)
        Order.objects.create(user=self.user2)
        Order.objects.create(user=self.user1)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_cannot_see_other_users_order_detail(self):
        other_order = Order.objects.create(user=self.user2)
        detail_url = reverse('order-detail', kwargs={'pk': other_order.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class AdminOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        setup_order_data(self)
        self.client.force_authenticate(self.admin_user)

    def test_admin_can_see_all_orders(self):
        Order.objects.create(user=self.user1)
        Order.objects.create(user=self.user2)
        Order.objects.create(user=self.user1)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_admin_can_see_any_order_detail(self):
        order = Order.objects.create(user=self.user1)
        detail_url = reverse('order-detail', kwargs={'pk': order.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)