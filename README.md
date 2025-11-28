# 🏝️ Туристическое агентство - API

Django REST API для управления турами, направлениями и бронированиями с JWT аутентификацией и Swagger документацией.

## 🚀 Возможности

- **🔐 JWT аутентификация** - безопасный доступ к API
- **📚 Swagger документация** - интерактивная документация API
- **🗺️ Управление направлениями** - страны, города, цены
- **🚌 Управление турами** - различные типы туров с датами
- **📅 Система бронирований** - бронирование туров пользователями
- **🔍 Фильтрация и поиск** - мощная система фильтрации данных
- **🐳 Docker поддержка** - легкий деплой и разработка

## 🛠 Технологии

- **Backend**: Django 4.2.7 + Django REST Framework
- **Аутентификация**: JWT (Simple JWT)
- **Документация**: DRF Spectacular (Swagger/OpenAPI)
- **База данных**: SQLite (разработка) / PostgreSQL (продакшен)
- **Контейнеризация**: Docker + Docker Compose
- **Фронтенд готовность**: CORS настроен для React/Vue.js

## 📦 Установка и запуск

### Локальная разработка

1. **Клонируй репозиторий**
git clone <repository-url>
cd turism

2. **Создай виртуальное окружение**
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

3. **Установи зависимости**
pip install -r requirements.txt

4. **Настрой базу данных**
python manage.py migrate
python manage.py createsuperuser

5. **Запусти сервер**
python manage.py runserver

### Docker разработка

1. **Собери и запусти контейнеры**
docker-compose up --build

2. **Выполни миграции (в отдельном терминале)**
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

## 🌐 API Endpoints

### 🔐 Аутентификация
- `POST /auth/token/` - Получить JWT токен
- `POST /auth/token/refresh/` - Обновить токен

### 🗺️ Направления (Destinations)
- `GET /destinations/` - Список направлений
- `POST /destinations/` - Создать направление (админ)
- `GET /destinations/{id}/` - Детали направления
- `PUT/PATCH /destinations/{id}/` - Обновить направление (админ)
- `DELETE /destinations/{id}/` - Удалить направление (админ)

### 🚌 Туры (Tours)
- `GET /tours/` - Список туров
- `POST /tours/` - Создать тур (админ)
- `GET /tours/{id}/` - Детали тура
- `PUT/PATCH /tours/{id}/` - Обновить тур (админ)
- `DELETE /tours/{id}/` - Удалить тур (админ)

### 📅 Бронирования (Bookings)
- `GET /bookings/` - Список бронирований (только свои)
- `POST /bookings/` - Создать бронирование
- `GET /bookings/{id}/` - Детали бронирования
- `PUT/PATCH /bookings/{id}/` - Обновить бронирование
- `DELETE /bookings/{id}/` - Удалить бронирование
- `POST /bookings/{id}/cancel/` - Отменить бронирование
- `GET /bookings/my/` - Мои бронирования

## 🔍 Параметры запросов

### Фильтрация
GET /tours/?tour_type=beach&destination__country=Турция
GET /bookings/?status=confirmed

### Сортировка
GET /destinations/?ordering=-price        # по убыванию цены
GET /tours/?ordering=start_date          # по дате начала
GET /bookings/?ordering=-booking_date    # новые сначала

### Поиск
GET /destinations/?search=париж          # поиск по названию, стране, городу
GET /tours/?search=экскурсия            # поиск по названию, описанию

### Пагинация
GET /destinations/?page=2                # вторая страница

## 📊 Модели данных

### 🗺️ Direction (Направление)
- `name` - Название направления
- `description` - Описание
- `country` - Страна
- `city` - Город
- `price` - Цена
- `duration_days` - Длительность (дни)
- `image` - Изображение
- `is_active` - Активно

### 🚌 Tour (Тур)
- `destination` - Направление (ForeignKey)
- `name` - Название тура
- `description` - Описание
- `tour_type` - Тип тура (пляжный, экскурсионный, экстремальный, культурный, шоппинг)
- `start_date` - Дата начала
- `end_date` - Дата окончания
- `available_slots` - Доступные места
- `max_slots` - Максимальное количество мест
- `is_active` - Активен

### 📅 Booking (Бронирование)
- `user` - Пользователь (ForeignKey)
- `tour` - Тур (ForeignKey)
- `booking_date` - Дата бронирования (авто)
- `number_of_people` - Количество человек (1-10)
- `total_price` - Общая стоимость (авторасчет)
- `status` - Статус (ожидание, подтверждено, отменено, завершено)
- `contact_phone` - Контактный телефон
- `contact_email` - Контактный email

## 🔐 Права доступа

- **Направления и туры**: Чтение - всем, запись - только админам
- **Бронирования**: Каждый пользователь видит только свои бронирования
- **Администраторы**: Полный доступ ко всем данным

## 🐳 Docker команды

# Запуск
docker-compose up --build

# Остановка
docker-compose down

# Миграции
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Просмотр логов
docker-compose logs -f web

## 📚 Документация

После запуска сервера документация доступна по адресам:
- **Swagger UI**: http://localhost:8000/swagger/
- **Админка**: http://localhost:8000/admin/



Этот README включает:
- 📋 Описание возможностей
- 🛠 Инструкции по установке
- 🌐 Полную документацию API
- 🔍 Примеры использования
- 🐳 Docker команды
- 📚 Ссылки на документацию

Готово для использования в твоем проекте! 🎯
