from django.contrib import admin
from .models import Destination, Tour, Booking

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'price', 'duration_days', 'is_active']
    list_filter = ['country', 'city', 'is_active']
    search_fields = ['name', 'country', 'city']
    list_editable = ['is_active']

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'destination', 'tour_type', 'start_date', 'end_date', 'available_slots', 'is_active']
    list_filter = ['tour_type', 'start_date', 'is_active']
    search_fields = ['name', 'destination__name']
    list_editable = ['is_active']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tour', 'booking_date', 'number_of_people', 'total_price', 'status']
    list_filter = ['status', 'booking_date']
    search_fields = ['user__username', 'tour__name']
    list_editable = ['status']