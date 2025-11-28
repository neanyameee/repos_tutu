from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from tutu.views import DestinationViewSet, TourViewSet, BookingViewSet

# Создаем схему API с разрешением доступа для всех
schema_view = SpectacularAPIView.as_view(
    permission_classes=(permissions.AllowAny,),  # Разрешаем доступ без авторизации
)

# Создаем отдельные роутеры для каждого раздела API

# Роутер для направлений (Destinations)
destinations_router = routers.DefaultRouter() # DefaultRouter автоматически генерирует стандартные CRUD endpoints
destinations_router.register(r'', DestinationViewSet, basename='destination')

# Роутер для туров (Tours)
tours_router = routers.DefaultRouter()
tours_router.register(r'', TourViewSet, basename='tour')

# Роутер для бронирований (Bookings)
bookings_router = routers.DefaultRouter()
bookings_router.register(r'', BookingViewSet, basename='booking')
# ↑ Создает endpoints:
# - GET/POST /bookings/              - список и создание бронирований
# - GET/PUT/PATCH/DELETE /bookings/{id}/ - работа с конкретным бронированием
# - POST /bookings/{id}/cancel/      - отмена бронирования (кастомный action)

# Основной список URL patterns проекта
urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),

    path('admin/', admin.site.urls),

    # Подключаем API endpoints для направлений
    path('destinations/', include(destinations_router.urls)),

    # Подключаем API endpoints для туров
    path('tours/', include(tours_router.urls)),

    # Подключаем API endpoints для бронирований
    path('bookings/', include(bookings_router.urls)),

    # Endpoint для получения JWT токена авторизации
    # POST /auth/token/ - отправляем {username, password}, получаем {access, refresh}
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint для обновления JWT токена
    # POST /auth/token/refresh/ - отправляем {refresh}, получаем новый {access}
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Генерация схемы OpenAPI в формате JSON
    # GET /schema/ - возвращает JSON с описанием всего API
    # Используется Swagger для построения документации
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI - интерактивная веб-документация API
    # Позволяет отправлять запросы прямо из браузера
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]