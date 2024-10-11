from django.apps import AppConfig


class QuadrosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quadros"
    
    def ready(self):
        import quadros.signals
