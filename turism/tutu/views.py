from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Destination, Tour, Booking
from .serializers import (
    DestinationSerializer,
    TourSerializer,
    BookingSerializer,
    BookingCreateSerializer
)

class DestinationViewSet(viewsets.ModelViewSet):

    # Базовый queryset - только активные направления
    queryset = Destination.objects.filter(is_active=True)

    # Сериализатор для преобразования данных
    serializer_class = DestinationSerializer

    # Системы фильтрации, поиска и сортировки
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['country', 'city']  # Фильтрация по стране и городу
    search_fields = ['name', 'description', 'country', 'city']  # Поля для поиска
    ordering_fields = ['price', 'duration_days', 'created_at']  # Поля для сортировки
    ordering = ['-created_at']  # Сортировка по умолчанию - новые сначала

    def get_permissions(self):
        """
        Динамическое определение прав доступа в зависимости от действия:
        - Чтение: доступно всем
        - Создание/изменение/удаление: только администраторам
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Только админы
        return [permissions.IsAuthenticatedOrReadOnly()]  # Чтение - всем, запись - авторизованным


class TourViewSet(viewsets.ModelViewSet):
    # Базовый queryset - только активные туры + предзагрузка связанного направления
    queryset = Tour.objects.filter(is_active=True).select_related('destination')

    # Сериализатор для туров
    serializer_class = TourSerializer

    # Системы фильтрации, поиска и сортировки
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tour_type', 'destination__country', 'destination__city']  # Фильтрация по типу и месту
    search_fields = ['name', 'description', 'destination__name']  # Поиск по названию тура и направления
    ordering_fields = ['start_date', 'end_date', 'destination__price']  # Сортировка по датам и цене
    ordering = ['-created_at']  # Новые туры первыми

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]


class BookingViewSet(viewsets.ModelViewSet):
    # Базовый queryset (будет переопределен в get_queryset)
    queryset = Booking.objects.all()

    # Сериализатор по умолчанию
    serializer_class = BookingSerializer

    # Все действия требуют авторизации
    permission_classes = [permissions.IsAuthenticated]

    # Системы фильтрации и сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']  # Фильтрация по статусу бронирования
    ordering_fields = ['booking_date', 'total_price']  # Сортировка по дате и цене
    ordering = ['-booking_date']  # Последние бронирования первыми

    def get_queryset(self):
        if self.request.user.is_staff:
            # Админы видят все бронирования с предзагрузкой связей
            return Booking.objects.all().select_related('user', 'tour', 'tour__destination')
        # Обычные пользователи видят только свои бронирования
        return Booking.objects.filter(user=self.request.user).select_related('user', 'tour', 'tour__destination')

    def get_serializer_class(self):
        """
        Выбор сериализатора в зависимости от действия:
        - При создании: BookingCreateSerializer (ограниченные поля)
        - В остальных случаях: BookingSerializer (все поля)
        """
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        """
        Автоматически привязывает текущего пользователя к бронированию при создании.
        Вызывается при сохранении нового объекта.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        # Кастомное действие для отмены бронирования.
        # Получаем конкретное бронирование
        booking = self.get_object()

        # Проверяем можно ли отменить (только бронирования в статусе 'ожидание')
        if booking.status == 'pending':
            # Меняем статус на 'отменено'
            booking.status = 'cancelled'
            booking.save()

            # Возвращаем успешный ответ
            return Response({'status': 'Бронирование отменено'})

        # Если статус не 'ожидание' - возвращаем ошибку
        return Response(
            {'error': 'Невозможно отменить бронирование с текущим статусом'},
            status=status.HTTP_400_BAD_REQUEST
        )