from django.apps import AppConfig

class WebFrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_front'

    def ready(self):
        import web_front.signals
