from django.apps import AppConfig


class StartAppConfig(AppConfig):
    name = "backend"

    def ready(self):
        # импортируем модуль со сигналами — чтобы регистрация сигналов произошла
        import backend.signals  # noqa: F401
