from django.contrib import admin
from .models import Destination, Tour, Booking

"""
настраивает интерфейс администратора Django.
как модели будут отображаться в админке.
"""

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в таблице списка направлений
    list_display = ['name', 'country', 'city', 'price', 'duration_days', 'is_active']
    # Поля по которым можно фильтровать список
    list_filter = ['country', 'city', 'is_active']
    # Поля по которым работает поиск
    search_fields = ['name', 'country', 'city']

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'destination', 'tour_type', 'start_date', 'end_date', 'available_slots', 'is_active']
    list_filter = ['tour_type', 'start_date', 'is_active']
    search_fields = ['name', 'destination__name']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Booking в админке.
    Определяет как выглядит список бронирований и их фильтрация.
    """
    list_display = ['id', 'user', 'tour', 'booking_date', 'number_of_people', 'total_price', 'status']
    list_filter = ['status', 'booking_date']
    search_fields = ['user__username', 'tour__name']