from django.apps import AppConfig


class AportalapiConfig(AppConfig):
    name = 'aportalapi'

    def ready(self):
        import aportalapi.models.user_utilities  # noqa: F401 — registers signals
