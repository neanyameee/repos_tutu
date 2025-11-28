from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

"""
Это файл models.py - он определяет структуру базы данных.
Каждый класс здесь становится таблицей в базе данных.
"""


class Destination(models.Model):
    """
    Модель 'Направление' - представляет туристическое направление
    Например: "Турция, Анталия" или "Египет, Хургада"
    """

    # Текстовое поле для названия направления (макс. 200 символов)
    name = models.CharField(max_length=200, verbose_name="Название направления")

    # Большое текстовое поле для подробного описания
    description = models.TextField(verbose_name="Описание")

    # Страна назначения
    country = models.CharField(max_length=100, verbose_name="Страна")

    # Город назначения
    city = models.CharField(max_length=100, verbose_name="Город")

    # Цена за тур (10 цифр всего, 2 после запятой)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    # Продолжительность тура в днях (только положительные числа)
    duration_days = models.PositiveIntegerField(verbose_name="Длительность (дни)")

    # Изображение направления (необязательное поле)
    image = models.ImageField(upload_to='destinations/', null=True, blank=True, verbose_name="Изображение")

    # Флаг активности - можно временно скрыть направление
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    # Автоматически устанавливается при создании записи
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        """Настройки отображения модели в админке"""
        verbose_name = "Направление"  # Название в единственном числе
        verbose_name_plural = "Направления"  # Название во множественном числе
        ordering = ['-created_at']  # Сортировка по убыванию даты создания

    def __str__(self):
        """
        Строковое представление объекта
        Например: "Турция, Анталия (Турция)"
        """
        return f"{self.name} ({self.country})"


class Tour(models.Model):
    """
    Модель 'Тур' - представляет конкретный тур в определенном направлении
    Например: "Пляжный отдых в Анталии" или "Экскурсии по Стамбулу"
    """

    # Список возможных типов туров
    TOUR_TYPES = [
        ('beach', 'Пляжный'),  # Отдых на пляже
        ('excursion', 'Экскурсионный'),  # Обзорные экскурсии
        ('extreme', 'Экстремальный'),  # Экстремальные виды отдыха
        ('cultural', 'Культурный'),  # Культурные программы
        ('shopping', 'Шоппинг'),  # Шоппинг-туры
    ]

    # Связь с направлением: один Direction - много Tours
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,  # При удалении направления удалятся все связанные туры
        related_name='tours',  # Обратная связь: direction.tours.all()
        verbose_name="Направление"
    )

    # Название конкретного тура
    name = models.CharField(max_length=200, verbose_name="Название тура")

    # Подробное описание тура
    description = models.TextField(verbose_name="Описание")

    # Тип тура из предопределенного списка
    tour_type = models.CharField(
        max_length=20,
        choices=TOUR_TYPES,  # Ограниченный выбор из списка
        verbose_name="Тип тура"
    )

    # Дата начала тура
    start_date = models.DateField(verbose_name="Дата начала")

    # Дата окончания тура
    end_date = models.DateField(verbose_name="Дата окончания")

    # Количество свободных мест
    available_slots = models.PositiveIntegerField(verbose_name="Доступные места")

    # Максимальная вместимость тура
    max_slots = models.PositiveIntegerField(verbose_name="Максимальное количество мест")

    # Флаг активности тура
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    # Дата создания записи
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        """Настройки отображения модели в админке"""
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ['-created_at']  # Новые туры первыми

    def __str__(self):
        """
        Строковое представление объекта
        Например: "Пляжный отдых в Анталии - Турция, Анталия"
        """
        return f"{self.name} - {self.destination.name}"


class Booking(models.Model):
    """
    Модель 'Бронирование' - представляет заказ тура пользователем
    Связывает пользователя, тур и информацию о бронировании
    """

    # Статусы бронирования
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),  # Ожидает подтверждения
        ('confirmed', 'Подтверждено'),  # Подтверждено менеджером
        ('cancelled', 'Отменено'),  # Отменено
        ('completed', 'Завершено'),  # Тур завершен
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

    # Автоматически устанавливается при создании бронирования
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")

    # Количество человек в бронировании (от 1 до 10)
    number_of_people = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),  # Не менее 1 человека
            MaxValueValidator(10)  # Не более 10 человек
        ],
        verbose_name="Количество человек"
    )

    # Общая стоимость = цена направления × количество человек
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")

    # Текущий статус бронирования
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',  # По умолчанию "ожидание"
        verbose_name="Статус"
    )

    # Контактный телефон для связи
    contact_phone = models.CharField(max_length=20, verbose_name="Контактный телефон")

    # Email для уведомлений
    contact_email = models.EmailField(verbose_name="Контактный email")

    class Meta:
        """Настройки отображения модели в админке"""
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-booking_date']  # Последние бронирования первыми

    def __str__(self):
        """
        Строковое представление объекта
        Например: "Бронирование #15 - admin"
        """
        return f"Бронирование #{self.id} - {self.user.username}"

    def save(self, *args, **kwargs):
        """
        Автоматически рассчитывает общую стоимость перед сохранением
        Вызывается каждый раз при создании или обновлении бронирования
        """
        # Если цена еще не рассчитана, рассчитываем ее
        if not self.total_price:
            # Общая стоимость = цена направления × количество человек
            self.total_price = self.tour.destination.price * self.number_of_people

        # Вызываем оригинальный метод save для сохранения в базу
        super().save(*args, **kwargs)