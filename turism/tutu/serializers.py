from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Destination, Tour, Booking

"""
Это файл serializers.py - он преобразует данные моделей Django в JSON 
и обратно для API. Сериализаторы определяют, какие поля будут отображаться 
в API и как они будут валидироваться.
"""


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя Django.
    Преобразует объект User в JSON для API ответов.
    """

    class Meta:
        model = User  # Указываем, какую модель сериализуем
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        # ↑ Какие поля пользователя будут включены в API ответ:
        # - id: уникальный идентификатор
        # - username: логин пользователя
        # - email: электронная почта
        # - first_name: имя
        # - last_name: фамилия


class DestinationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Направления.
    Преобразует объект Destination в JSON.
    """

    class Meta:
        model = Destination  # Связываем с моделью Direction
        fields = '__all__'  # Включаем ВСЕ поля из модели в API
        # Автоматически будут включены:
        # id, name, description, country, city, price, duration_days,
        # image, is_active, created_at


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
        fields = '__all__'  # Все поля модели + вычисляемые поля выше
        # Будут включены:
        # - Все поля модели Tour (id, name, description, tour_type, и т.д.)
        # - destination_name (название направления)
        # - destination_country (страна направления)


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
        read_only=True  # Только для чтения
    )

    # Вычисляемое поле - название направления через тур
    destination_name = serializers.CharField(
        source='tour.destination.name',  # Цепочка: тур → направление → название
        read_only=True  # Только для чтения
    )

    class Meta:
        model = Booking  # Связываем с моделью Booking
        fields = '__all__'  # Все поля + вычисляемые поля выше
        read_only_fields = ['user', 'booking_date', 'total_price']
        # ↑ Поля, которые нельзя изменить через API:
        # - user: устанавливается автоматически из текущего пользователя
        # - booking_date: устанавливается автоматически при создании
        # - total_price: рассчитывается автоматически при сохранении


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для СОЗДАНИЯ бронирований.
    Используется когда нужно СОЗДАТЬ новое бронирование.
    Ограничивает поля, которые можно указать при создании.
    """

    class Meta:
        model = Booking  # Связываем с моделью Booking
        fields = ['tour', 'number_of_people', 'contact_phone', 'contact_email']
        # Только эти поля можно указать при создании бронирования:
        # - tour: какой тур бронируем (обязательно)
        # - number_of_people: количество человек (обязательно)
        # - contact_phone: телефон для связи (обязательно)
        # - contact_email: email для уведомлений (обязательно)

        # НЕ включены (устанавливаются автоматически):
        # - user: берется из текущего авторизованного пользователя
        # - booking_date: текущая дата и время
        # - total_price: рассчитывается из цены тура и количества человек
        # - status: по умолчанию "ожидание"