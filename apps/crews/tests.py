from apps.users.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Crew


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.list_url = reverse("crew-list")
        self.detail_url = reverse("crew-detail", kwargs={"pk": self.crew.pk})

    def test_crew_list_unauthorized(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpass123"
        )
        self.client.force_authenticate(self.user)
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.list_url = reverse("crew-list")
        self.detail_url = reverse("crew-detail", kwargs={"pk": self.crew.pk})

    def test_can_list_crews(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_cannot_create_crew(self):
        data = {"first_name": "Jane", "last_name": "Smith"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@test.com", password="adminpass123", is_staff=True
        )
        self.client.force_authenticate(self.admin_user)
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.list_url = reverse("crew-list")
        self.detail_url = reverse("crew-detail", kwargs={"pk": self.crew.pk})

    def test_admin_can_create_crew(self):
        data = {"first_name": "Jane", "last_name": "Smith"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Crew.objects.count(), 2)
