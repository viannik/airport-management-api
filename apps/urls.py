# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.airports.views import AirportViewSet
from apps.airplanes.views import AirplaneViewSet, AirplaneTypeViewSet
from apps.flights.views import FlightViewSet, RouteViewSet
from apps.crews.views import CrewViewSet
from apps.tickets.views import TicketViewSet
from apps.orders.views import OrderViewSet

router = DefaultRouter()
router.register(r"airports", AirportViewSet)
router.register(r"airplanes", AirplaneViewSet)
router.register(r"airplane-types", AirplaneTypeViewSet)
router.register(r"flights", FlightViewSet)
router.register(r"routes", RouteViewSet)
router.register(r"crews", CrewViewSet)
router.register(r"tickets", TicketViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]
