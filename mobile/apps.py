from django.apps import AppConfig


class MobileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mobile'


from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'mobile'

    def ready(self):
        import mobile.signals  # Import des signals pour que Django puisse les écouter
