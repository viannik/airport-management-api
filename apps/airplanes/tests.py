from apps.users.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Airplane, AirplaneType


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="UA-001", rows=30, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.list_url = reverse("airplane-list")
        self.detail_url = reverse("airplane-detail", kwargs={"pk": self.airplane.pk})

    def test_airplane_list_unauthorized(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpass123"
        )
        self.client.force_authenticate(self.user)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="UA-001", rows=30, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.list_url = reverse("airplane-list")
        self.detail_url = reverse("airplane-detail", kwargs={"pk": self.airplane.pk})

    def test_can_list_airplanes(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_cannot_create_airplane(self):
        data = {
            "name": "UA-002",
            "rows": 25,
            "seats_in_row": 4,
            "airplane_type": self.airplane_type.name,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@test.com", password="adminpass123", is_staff=True
        )
        self.client.force_authenticate(self.admin_user)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.list_url = reverse("airplane-list")

    def test_admin_can_create_airplane(self):
        data = {
            "name": "UA-002",
            "rows": 25,
            "seats_in_row": 4,
            "airplane_type": self.airplane_type.name,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

