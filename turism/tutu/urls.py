from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from tutu.views import DestinationViewSet, TourViewSet, BookingViewSet


# Создаем автоматический маршрутизатор для REST API
# DRF Router автоматически создает стандартные CRUD endpoints для ViewSet'ов
router = routers.DefaultRouter()

# Регистрируем ViewSet'ы в роутере - создаем автоматические URL patterns:
router.register(r'destinations', DestinationViewSet)  # Создает:

router.register(r'tours', TourViewSet)  # Создает:

router.register(r'bookings', BookingViewSet)  # Создает:

# Основной список маршрутов Django
urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),

    path('admin/', admin.site.urls),

    # Подключаем все автоматически созданные API endpoints из роутера

    path('api/', include(router.urls)),

    # Endpoint для получения JWT токена авторизации
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint для обновления JWT токена
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Генерация схемы OpenAPI/Swagger в формате JSON
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
