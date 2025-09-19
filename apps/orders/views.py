from rest_framework import filters, viewsets

from .models import Order
from .serializers import OrderSerializer, OrderListSerializer
from apps.permissions import IsAuthenticatedOrAdmin

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related('user').all()
    permission_classes = [IsAuthenticatedOrAdmin]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'user__username']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)