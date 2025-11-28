from django.apps import AppConfig


class TutuConfig(AppConfig):
    """
    Конфигурация Django приложения определяет настройки и метаданные приложения.
    Django автоматически находит и загружает этот класс при запуске.
    """
    # Тип поля для автоматического создания первичных ключей
    default_auto_field = 'django.db.models.BigAutoField' # BigAutoField создает 64-битные целые числа (от 1 до 9223372036854775807)
    name = 'tutu'
    verbose_name = 'Туристическое агентство Tutu'