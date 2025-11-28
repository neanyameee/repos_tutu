from django.contrib import admin
from .models import Destination, Tour, Booking

"""
Это файл admin.py - настраивает интерфейс администратора Django.
Здесь мы определяем, как модели будут отображаться в админке.
"""


# Декоратор @admin.register автоматически регистрирует модель в админке
# Вместо: admin.site.register(Destination, DestinationAdmin)

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Direction в админке.
    Определяет как выглядит список направлений и их фильтрация.
    """

    # Поля, которые будут отображаться в таблице списка направлений
    list_display = ['name', 'country', 'city', 'price', 'duration_days', 'is_active']
    # ↑ Отображает колонки:
    # - name: название направления
    # - country: страна
    # - city: город
    # - price: цена
    # - duration_days: длительность в днях
    # - is_active: активность (галочка)

    # Поля по которым можно фильтровать список (появляется справа)
    list_filter = ['country', 'city', 'is_active']
    # ↑ Фильтры для:
    # - country: выбор страны из существующих
    # - city: выбор города из существующих
    # - is_active: фильтр по активности

    # Поля по которым работает поиск (появляется сверху)
    search_fields = ['name', 'country', 'city']
    # ↑ Поиск будет искать совпадения в:
    # - name: названии направления
    # - country: названии страны
    # - city: названии города


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Tour в админке.
    Определяет как выглядит список туров и их фильтрация.
    """

    # Поля для отображения в таблице списка туров
    list_display = ['name', 'destination', 'tour_type', 'start_date', 'end_date', 'available_slots', 'is_active']
    # ↑ Отображает колонки:
    # - name: название тура
    # - destination: связанное направление (показывает __str__ модели Direction)
    # - tour_type: тип тура
    # - start_date: дата начала
    # - end_date: дата окончания
    # - available_slots: доступные места
    # - is_active: активность тура

    # Фильтры для туров
    list_filter = ['tour_type', 'start_date', 'is_active']
    # ↑ Фильтры по:
    # - tour_type: типу тура (пляжный, экскурсионный и т.д.)
    # - start_date: дате начала (автоматически группирует по датам)
    # - is_active: активности

    # Поля для поиска
    search_fields = ['name', 'destination__name']
    # ↑ Поиск по:
    # - name: названию тура
    # - destination__name: названию связанного направления (через ForeignKey)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Booking в админке.
    Определяет как выглядит список бронирований и их фильтрация.
    """

    # Поля для отображения в таблице бронирований
    list_display = ['id', 'user', 'tour', 'booking_date', 'number_of_people', 'total_price', 'status']
    # ↑ Отображает колонки:
    # - id: номер бронирования
    # - user: пользователь (показывает username)
    # - tour: связанный тур (показывает __str__ модели Tour)
    # - booking_date: дата бронирования
    # - number_of_people: количество человек
    # - total_price: общая стоимость
    # - status: статус бронирования

    # Фильтры для бронирований
    list_filter = ['status', 'booking_date']
    # ↑ Фильтры по:
    # - status: статусу (ожидание, подтверждено, отменено, завершено)
    # - booking_date: дате бронирования (автоматически группирует по датам)

    # Поля для поиска
    search_fields = ['user__username', 'tour__name']
    # ↑ Поиск по:
    # - user__username: имени пользователя (через ForeignKey)
    # - tour__name: названию связанного тура (через ForeignKey)