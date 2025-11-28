from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Destination, Tour, Booking

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя Django.
    Преобразует объект User в JSON для API ответов.
    """
    class Meta:
        model = User  # Указываем, какую модель сериализуем
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] # Какие поля пользователя будут включены в API ответ:


class DestinationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Направления.
    Преобразует объект Destination в JSON.
    """

    class Meta:
        model = Destination  # Связываем с моделью Direction
        fields = '__all__'  # Включаем ВСЕ поля из модели в API


class TourSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Тура.
    Добавляет вычисляемые поля для удобства отображения в API.
    """

    # Вычисляемое поле - название направления (не сохраняется в БД)
    destination_name = serializers.CharField(
        source='destination.name',  # Берем значение из связанного объекта Direction
        read_only=True  # Только для чтения, нельзя изменить через API
    )

    # Вычисляемое поле - страна направления
    destination_country = serializers.CharField(
        source='destination.country',  # Берем страну из связанного Direction
        read_only=True  # Только для чтения
    )

    class Meta:
        model = Tour  # Связываем с моделью Tour
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ЧТЕНИЯ бронирований.
    Используется когда нужно ПОЛУЧИТЬ информацию о бронировании.
    Включает подробную информацию о связанных объектах.
    """
    # Вложенный сериализатор - полная информация о пользователе
    user = UserSerializer(
        read_only=True  # Только для чтения, нельзя изменить через API
    )

    # Вычисляемое поле - название тура
    tour_name = serializers.CharField(
        source='tour.name',  # Берем название из связанного тура
        read_only=True
    )
    # Вычисляемое поле - название направления через тур
    destination_name = serializers.CharField(
        source='tour.destination.name',
        read_only=True
    )

    class Meta:
        model = Booking  # Связываем с моделью Booking
        fields = '__all__'  # Все поля
        read_only_fields = ['user', 'booking_date', 'total_price'] # Поля, которые нельзя изменить через API: user, booking_date, total_price

class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для СОЗДАНИЯ бронирований.
    Используется когда нужно СОЗДАТЬ новое бронирование.
    Ограничивает поля, которые можно указать при создании.
    """

    class Meta:
        model = Booking  # Связываем с моделью Booking
        fields = ['tour', 'number_of_people', 'contact_phone', 'contact_email'] # Только эти поля можно указать при создании бронирования: tour, number_of_people, contact_phone, contact_email
        # НЕ включены user,booking_date,total_price,status