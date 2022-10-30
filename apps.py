from django.apps import AppConfig


class NewscraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newscraper'


class NewscraperCaching(AppConfig):
    name = 'newscraper_cache'

    def ready(self):
        import signals
