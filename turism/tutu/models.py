from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Destination(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название направления")
    description = models.TextField(verbose_name="Описание")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_days = models.PositiveIntegerField(verbose_name="Длительность (дни)")
    image = models.ImageField(upload_to='destinations/', null=True, blank=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.country})"

class Tour(models.Model):
    TOUR_TYPES = [
        ('beach', 'Пляжный'),
        ('excursion', 'Экскурсионный'),
        ('extreme', 'Экстремальный'),
        ('cultural', 'Культурный'),
        ('shopping', 'Шоппинг'),
    ]

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tours', verbose_name="Направление")
    name = models.CharField(max_length=200, verbose_name="Название тура")
    description = models.TextField(verbose_name="Описание")
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES, verbose_name="Тип тура")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    available_slots = models.PositiveIntegerField(verbose_name="Доступные места")
    max_slots = models.PositiveIntegerField(verbose_name="Максимальное количество мест")
    includes = models.TextField(verbose_name="Что включено")
    excludes = models.TextField(verbose_name="Что не включено")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.destination.name}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings', verbose_name="Тур")
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    number_of_people = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Количество человек"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    special_requests = models.TextField(blank=True, verbose_name="Особые пожелания")
    contact_phone = models.CharField(max_length=20, verbose_name="Контактный телефон")
    contact_email = models.EmailField(verbose_name="Контактный email")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-booking_date']

    def __str__(self):
        return f"Бронирование #{self.id} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.tour.destination.price * self.number_of_people
        super().save(*args, **kwargs)