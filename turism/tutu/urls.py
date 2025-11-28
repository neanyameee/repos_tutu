from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from tutu.views import DestinationViewSet, TourViewSet, BookingViewSet

"""
Это главный файл маршрутизации (URL configuration) Django.
Он определяет, какие URL ведут на какие страницы и API endpoints.
"""

# Создаем автоматический маршрутизатор для REST API
# DRF Router автоматически создает стандартные CRUD endpoints для ViewSet'ов
router = routers.DefaultRouter()

# Регистрируем ViewSet'ы в роутере - создаем автоматические URL patterns:
router.register(r'destinations', DestinationViewSet)  # Создает:
# GET/POST /api/destinations/     - список и создание направлений
# GET/PUT/PATCH/DELETE /api/destinations/{id}/ - операции с конкретным направлением

router.register(r'tours', TourViewSet)  # Создает:
# GET/POST /api/tours/            - список и создание туров
# GET/PUT/PATCH/DELETE /api/tours/{id}/ - операции с конкретным туром

router.register(r'bookings', BookingViewSet)  # Создает:
# GET/POST /api/bookings/         - список и создание бронирований
# GET/PUT/PATCH/DELETE /api/bookings/{id}/ - операции с конкретным бронированием

# Основной список маршрутов Django
urlpatterns = [
    # Редирект с корневой страницы на Swagger документацию
    # Когда пользователь заходит на http://127.0.0.1:8000/ - его перенаправляет на /swagger/
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),

    # Административная панель Django
    # Доступна по адресу: http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),

    # Подключаем все автоматически созданные API endpoints из роутера
    # Все endpoints будут доступны по префиксу /api/
    # Например: /api/destinations/, /api/tours/, /api/bookings/
    path('api/', include(router.urls)),

    # Endpoint для получения JWT токена авторизации
    # POST /api/auth/token/ - отправляем username и password, получаем access/refresh токены
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint для обновления JWT токена
    # POST /api/auth/token/refresh/ - отправляем refresh токен, получаем новый access токен
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Генерация схемы OpenAPI/Swagger в формате JSON
    # GET /api/schema/ - возвращает JSON с описанием всего API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI - интерактивная документация API
    # GET /swagger/ - красивый веб-интерфейс для тестирования API
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
