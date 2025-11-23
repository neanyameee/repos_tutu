from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Destination, Tour, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_country = serializers.CharField(source='destination.country', read_only=True)
    destination_city = serializers.CharField(source='destination.city', read_only=True)
    destination_price = serializers.DecimalField(source='destination.price', read_only=True, max_digits=10,
                                                 decimal_places=2)

    class Meta:
        model = Tour
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tour_name = serializers.CharField(source='tour.name', read_only=True)
    destination_name = serializers.CharField(source='tour.destination.name', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'booking_date', 'total_price']


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['tour', 'number_of_people', 'special_requests', 'contact_phone', 'contact_email']