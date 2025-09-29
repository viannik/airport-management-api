from apps.users.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Airport


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.airport = Airport.objects.create(
            name="Test Airport", closest_big_city="Test City"
        )
        self.list_url = reverse("airport-list")
        self.detail_url = reverse("airport-detail", kwargs={"pk": self.airport.pk})

    def test_airport_list_unauthorized(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpass123"
        )
        self.client.force_authenticate(self.user)
        self.airport = Airport.objects.create(
            name="Test Airport", closest_big_city="Test City"
        )
        self.list_url = reverse("airport-list")
        self.detail_url = reverse("airport-detail", kwargs={"pk": self.airport.pk})

    def test_cannot_create_airport(self):
        data = {"name": "New Airport", "closest_big_city": "New City"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@test.com", password="adminpass123", is_staff=True
        )
        self.client.force_authenticate(self.admin_user)
        self.airport = Airport.objects.create(
            name="Test Airport", closest_big_city="Test City"
        )
        self.list_url = reverse("airport-list")
        self.detail_url = reverse("airport-detail", kwargs={"pk": self.airport.pk})

    def test_admin_can_create_airport(self):
        data = {"name": "New Airport", "closest_big_city": "New City"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 2)
