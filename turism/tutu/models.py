from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

"""
models.py определяет структуру базы данных.
Каждый класс здесь становится таблицей в базе данных.
"""

class Destination(models.Model):
    """
    Модель 'Направление' - представляет туристическое направление
    Например: "Турция, Анталия" или "Египет, Хургада"
    """

    name = models.CharField(max_length=200, verbose_name="Название направления")
    description = models.TextField(verbose_name="Описание")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_days = models.PositiveIntegerField(verbose_name="Длительность (дни)")
    image = models.ImageField(upload_to='destinations/', null=True, blank=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        """Настройки отображения модели в админке"""
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
        ordering = ['-created_at']  # Сортировка по убыванию даты создания

    def __str__(self):
        return f"{self.name} ({self.country})"


class Tour(models.Model):
    """
    Модель 'Тур' - представляет конкретный тур в определенном направлении
    Например: "Пляжный отдых в Анталии" или "Экскурсии по Стамбулу"
    """
    # Список возможных типов туров
    TOUR_TYPES = [
        ('beach', 'Пляжный'),
        ('excursion', 'Экскурсионный'),
        ('extreme', 'Экстремальный'),
        ('cultural', 'Культурный'),
        ('shopping', 'Шоппинг'),
    ]

    # Связь с направлением
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,  # При удалении направления удалятся все связанные туры
        related_name='tours',  # Обратная связь: direction.tours.all()
        verbose_name="Направление"
    )

    name = models.CharField(max_length=200, verbose_name="Название тура")
    description = models.TextField(verbose_name="Описание")
    tour_type = models.CharField(
        max_length=20,
        choices=TOUR_TYPES,  # Ограниченный выбор из списка
        verbose_name="Тип тура"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    # Количество свободных мест
    available_slots = models.PositiveIntegerField(verbose_name="Доступные места")
    # Максимальная вместимость тура
    max_slots = models.PositiveIntegerField(verbose_name="Максимальное количество мест")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ['-created_at']

    def __str__(self):
        """
        Строковое представление объекта
        """
        return f"{self.name} - {self.destination.name}"


class Booking(models.Model):
    """
    Модель 'Бронирование' - представляет заказ тура пользователем
    Связывает пользователя, тур и информацию о бронировании
    """
    # Статусы бронирования
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]

    # Связь с пользователем Django
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении пользователя удалятся его бронирования
        related_name='bookings',  # Обратная связь: user.bookings.all()
        verbose_name="Пользователь"
    )
    # Связь с туром
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,  # При удалении тура удалятся связанные бронирования
        related_name='bookings',  # Обратная связь: tour.bookings.all()
        verbose_name="Тур"
    )
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    number_of_people = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name="Количество человек"
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',  # По умолчанию ожидание
        verbose_name="Статус"
    )

    contact_phone = models.CharField(max_length=20, verbose_name="Контактный телефон")
    contact_email = models.EmailField(verbose_name="Контактный email")
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-booking_date']

    def __str__(self):
        return f"Бронирование #{self.id} - {self.user.username}"

    def save(self, *args, **kwargs):
        #Автоматически рассчитывает общую стоимость перед сохранением, Вызывается каждый раз при создании или обновлении бронирования
        if not self.total_price:
            self.total_price = self.tour.destination.price * self.number_of_people
        # Вызываем метод save для сохранения в базу
        super().save(*args, **kwargs)