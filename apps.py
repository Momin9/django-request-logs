from django.apps import AppConfig

class RequestLogsConfig(AppConfig):
    """
    Configuration class for the Request Logs app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'request_logs'
