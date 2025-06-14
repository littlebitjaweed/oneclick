from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.core.management import call_command


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    # def ready(self):
    #     import app.signals

       