from django.apps import apps
from django.core.cache import cache
from django.test import TestCase

from newscraper.apps import NewscraperConfig, NewscraperCaching
from newscraper.models import Article, Symbol, ArticleComment, Wordcount


class NewscraperAppsTest(TestCase):

    def test_newscraper_config(self):
        self.assertEqual(NewscraperConfig.name, 'newscraper')
        self.assertEqual(apps.get_app_config('newscraper').name, 'newscraper')

    def test_newscraper_caching(self):
        self.assertEqual(NewscraperCaching.name, 'newscraper_cache')
