from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.core.management import call_command


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals

        try:
            from django.contrib.auth.models import User
            if not User.objects.exists():  # Only load if DB is empty
                call_command('loaddata', 'fixtures/data.json')
        except (OperationalError, ProgrammingError):
            # Happens during first migration — ignore safely
            pass