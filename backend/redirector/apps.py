from django.apps import AppConfig


class RedirectorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "redirector"

    def ready(self):
        from . import signals  # noqa
