from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Destination, Tour, Booking
from .serializers import (
    DestinationSerializer,
    TourSerializer,
    BookingSerializer,
    BookingCreateSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.filter(is_active=True)
    serializer_class = DestinationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    #filterset_fields = ['country', 'city']
    search_fields = ['name', 'description', 'country', 'city']
    ordering_fields = ['price', 'duration_days', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.filter(is_active=True).select_related('destination')
    serializer_class = TourSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    #filterset_fields = ['tour_type']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]


class BookingViewSet(viewsets.ModelViewSet):
    # Добавляем queryset по умолчанию
    queryset = Booking.objects.all().select_related('user', 'tour', 'tour__destination')
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['booking_date', 'total_price']
    ordering = ['-booking_date']

    def get_queryset(self):
        # Переопределяем get_queryset для фильтрации по пользователю
        if self.request.user.is_staff:
            return Booking.objects.all().select_related('user', 'tour', 'tour__destination')
        return Booking.objects.filter(user=self.request.user).select_related('user', 'tour', 'tour__destination')

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == 'pending':
            booking.status = 'cancelled'
            booking.save()
            return Response({'status': 'Бронирование отменено'})
        return Response(
            {'error': 'Невозможно отменить бронирование с текущим статусом'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        bookings = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)