from django.apps import AppConfig


class EDiaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'e_diary'

    def ready(self):
        import e_diary.signals  # noqa: F401
